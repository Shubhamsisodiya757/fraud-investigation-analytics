# Checkpoint 01 — Validation Notes

## Validation status

The synthetic dataset was evaluated using an equivalent implementation of the production rule to verify the expected alert set and edge-case behaviour.

A PostgreSQL server was not available in the execution environment, so this is a **logic validation**, not a claim of direct PostgreSQL execution.

## Observed alert set from equivalent logic

The following customer-beneficiary relationships produced `velocity_alert = 1`:

- C001 → B001
- C003 → B003
- C004 → B004
- C005 → B005
- C006 → B006
- C009 → B009

The observed alert set matches `checkpoint-01/expected-alerts.csv`.

## Important edge-case results

### C003 → B003

A rapid three-transaction sequence is followed by a later transaction with a 17-minute gap. The rapid sequence is preserved as the alerting burst; the later isolated transaction does not expand the burst.

### C004 → B004

The velocity rule correctly alerts on four rapid transactions. This is intentionally treated as a **false-positive candidate**, demonstrating that a detection rule is not equivalent to a fraud conclusion.

### C006 → B006

Transactions cross midnight but remain inside the 30-minute monitoring window. The rule correctly treats them as one sequence.

### C007 → B007

The first transaction occurs exactly 30 minutes after beneficiary creation and is included by the `<= 30 minutes` boundary condition. The subsequent transactions occur after the window and therefore do not create a three-transaction velocity alert.

### C008 → B008

A transaction before beneficiary creation is excluded. The remaining transactions have gaps greater than three minutes, so no velocity alert is generated.

### C009

The customer has two beneficiaries. B009 produces an alert while B010 does not, confirming that the analysis is partitioned at the customer-beneficiary level rather than incorrectly mixing the customer's beneficiaries.

## Next validation improvement

The next version should run the SQL directly in a PostgreSQL environment and add automated assertions for the expected alert set.
