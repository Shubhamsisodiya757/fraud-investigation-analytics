-- Checkpoint 01: Beneficiary Velocity Alert
-- SQL dialect: PostgreSQL
-- Purpose:
-- Identify customer-beneficiary relationships with potentially suspicious
-- transaction velocity shortly after beneficiary creation.
--
-- Rule:
-- 1. Transactions occur after beneficiary creation and within 30 minutes.
-- 2. A qualifying burst contains at least 3 transactions.
-- 3. A burst is formed by consecutive transaction gaps of <= 3 minutes.
-- 4. The result is an investigation alert, not a fraud conclusion.

WITH qualifying_txns AS (
    SELECT
        b.customer_id,
        b.beneficiary_account,
        b.added_on,
        t.txn_time,
        t.amount
    FROM beneficiaries b
    INNER JOIN transactions t
        ON b.customer_id = t.customer_id
        AND b.beneficiary_account = t.to_account
    WHERE t.txn_time > b.added_on
      AND t.txn_time <= b.added_on + INTERVAL '30 minutes'
),

lagged AS (
    SELECT
        customer_id,
        beneficiary_account,
        added_on,
        txn_time,
        amount,
        LAG(txn_time) OVER (
            PARTITION BY customer_id, beneficiary_account, added_on
            ORDER BY txn_time
        ) AS previous_txn_time
    FROM qualifying_txns
),

flagged AS (
    SELECT
        customer_id,
        beneficiary_account,
        added_on,
        txn_time,
        amount,
        previous_txn_time,
        CASE
            WHEN previous_txn_time IS NULL THEN 0
            WHEN EXTRACT(EPOCH FROM (txn_time - previous_txn_time)) / 60 <= 3 THEN 1
            ELSE 0
        END AS rapid_gap_flag
    FROM lagged
),

sequence_groups AS (
    SELECT
        customer_id,
        beneficiary_account,
        added_on,
        txn_time,
        amount,
        rapid_gap_flag,
        SUM(
            CASE
                WHEN rapid_gap_flag = 0 THEN 1
                ELSE 0
            END
        ) OVER (
            PARTITION BY customer_id, beneficiary_account, added_on
            ORDER BY txn_time
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS sequence_id
    FROM flagged
),

burst_summary AS (
    SELECT
        customer_id,
        beneficiary_account,
        added_on,
        sequence_id AS burst_id,
        MIN(txn_time) AS burst_start_time,
        MAX(txn_time) AS burst_end_time,
        COUNT(*) AS txns_in_burst,
        SUM(amount) AS total_burst_amount
    FROM sequence_groups
    GROUP BY
        customer_id,
        beneficiary_account,
        added_on,
        sequence_id
)

SELECT
    customer_id,
    beneficiary_account,
    added_on,
    burst_id,
    burst_start_time,
    burst_end_time,
    txns_in_burst,
    total_burst_amount,
    CASE
        WHEN txns_in_burst >= 3 THEN 1
        ELSE 0
    END AS velocity_alert
FROM burst_summary
ORDER BY
    customer_id,
    beneficiary_account,
    added_on,
    burst_id;
