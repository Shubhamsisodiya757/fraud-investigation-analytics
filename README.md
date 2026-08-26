# Fraud Investigation & Transaction Risk Analytics

A portfolio project for learning and demonstrating fraud-investigation reasoning, advanced SQL, transaction analytics, behavioural anomaly detection, and risk-scoring concepts.

## Project methodology

**Business problem → fraud hypothesis → required evidence → SQL analysis → risk signal → investigation priority**

The project uses synthetic financial data only. No real customer or financial information is included.

## Current checkpoints

- **Checkpoint 01 — Beneficiary Velocity Detection** ✅
- Checkpoint 02 — Customer Behavioural Baselines ⏳
- Checkpoint 03 — Account Takeover Analytics ⏳
- Checkpoint 04 — Mule / Network Detection ⏳
- Checkpoint 05 — Composite Risk Scoring ⏳

## Checkpoint 01

The first detection rule identifies potentially suspicious transaction velocity after a new beneficiary is added.

Rule version 1:

- Transaction occurs after beneficiary creation and within 30 minutes.
- At least 3 transactions form a qualifying sequence.
- Consecutive transaction gaps are 3 minutes or less.

The alert prioritizes an investigation; it does not establish fraud by itself.

See [`checkpoint-01/`](checkpoint-01/) for the investigation logic and SQL.

## Practice dataset

The repository includes a reproducible PostgreSQL synthetic dataset generator under [`datasets/postgresql/`](datasets/postgresql/).

The environment contains:

- 200 customers
- 200 accounts
- 411 beneficiaries
- 2,342 transactions
- 400 devices
- 1,004 login events
- 11 planted test scenarios

The dataset deliberately includes both suspicious-looking and legitimate-looking patterns so false positives can be studied instead of simply flagging everything.

## SQL skills being developed

- Multi-table JOINs
- CTEs
- `ROW_NUMBER()`
- `LAG()` / sequencing
- `COUNT() OVER`
- Running window calculations
- Time-window analysis
- Sequence / burst detection
- Behavioural baselines
- Composite risk scoring

## Data notice

All data in this repository is synthetic and created for portfolio, learning, and SQL practice purposes.
