# Checkpoint 01 — Beneficiary Velocity Detection

## Business Problem

Identify potentially suspicious transaction behaviour occurring shortly after a new beneficiary is added to a customer's account.

## Fraud Hypothesis

A compromised account may show rapid movement of funds shortly after a new beneficiary is created. The pattern becomes more concerning when multiple transactions occur in a short period and other independent risk signals are present.

## Detection Logic

**Version 1 — Beneficiary Velocity Rule**

Flag a customer-beneficiary relationship for further investigation when:

1. A new beneficiary is added.
2. Transactions are sent to that beneficiary after creation.
3. Transactions occur within the first 30 minutes after beneficiary creation.
4. At least 3 transactions occur in that window.
5. At least 2 consecutive transaction gaps are 3 minutes or less.

This rule is a detection signal, not proof of fraud.

## Supporting Risk Signals

The velocity rule can be strengthened by independent indicators such as:

- New or previously unseen device
- Unusual transaction time relative to the customer's normal behaviour
- Repeated identical transaction amounts
- Transaction amount materially above the customer's historical baseline

These signals should contribute to a composite risk assessment rather than individually prove fraud.

## Investigation Methodology

The investigation was designed before the SQL implementation:

**Business question → fraud hypothesis → required evidence → SQL analysis → risk signal → investigation priority**

This prevents SQL from becoming an exercise in syntax without an investigative objective.

## SQL Concepts Demonstrated

- Multi-column `INNER JOIN`
- Common Table Expressions (CTEs)
- `ROW_NUMBER()` for first-event identification
- `COUNT(*) OVER` for transaction counts without collapsing transaction rows
- `LAG()` for transaction sequencing
- Time-interval analysis
- Running `SUM()` for burst/sequence identification
- `GROUP BY` for burst-level summaries
- Rule-based risk scoring concepts

## Key Analytical Lessons

### 1. Customer context matters

A fixed monetary threshold is weak on its own. A transaction should be assessed relative to the customer's historical behaviour whenever possible.

### 2. One signal is rarely enough

A new device, unusual time, repeated amount, or rapid transaction pattern can each have legitimate explanations. Multiple independent signals provide stronger evidence.

### 3. Detection is not investigation

A high-risk alert prioritizes a case. It does not establish that fraud occurred. Further evidence such as authentication history, device information, beneficiary history, customer behaviour, and case context is required.

### 4. Event sequencing matters

`LAG()` lets the analyst compare an event with the immediately preceding event. This enables time-gap and velocity analysis.

### 5. Bursts are different from simple counts

Two customer-beneficiary relationships can have the same transaction count but very different concentrations of activity. Sequence analysis helps distinguish these patterns.

## Status

- [x] Define fraud hypothesis
- [x] Define beneficiary velocity rule
- [x] Build beneficiary-to-transaction join
- [x] Build 30-minute investigation window
- [x] Build transaction sequencing with `LAG()`
- [x] Build rapid-gap flag
- [x] Build burst-start and burst-ID logic
- [ ] Finalize production-ready velocity alert SQL
- [ ] Add synthetic dataset
- [ ] Add test scenarios and findings

## Data Notice

This portfolio project will use synthetic financial data. No real customer, account, or transaction data is included.
