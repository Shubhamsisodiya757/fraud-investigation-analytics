# Checkpoint 01 — Test Cases

The synthetic dataset is designed to test the Beneficiary Velocity Rule against both suspicious and legitimate-looking behaviour.

## Detection rule under test

Flag a customer-beneficiary relationship when:

- transactions occur after beneficiary creation;
- transactions occur within 30 minutes of beneficiary creation;
- at least 3 transactions form a qualifying sequence; and
- consecutive transaction gaps in that sequence are 3 minutes or less.

The result is an investigation alert, not a fraud conclusion.

## Expected scenarios

| Case | Customer | Beneficiary | Expected outcome | Reason |
|---|---|---|---|---|
| TC01 | C001 | B001 | Alert | 3 transactions at 02:05, 02:07 and 02:09; two rapid gaps of 2 minutes |
| TC02 | C002 | B002 | No alert | 3 transactions within 30 minutes, but gaps are 19 and 9 minutes |
| TC03 | C003 | B003 | Alert | 3-transaction rapid burst followed by a later non-rapid transaction |
| TC04 | C004 | B004 | Alert / False-positive candidate | 4 rapid transactions; pattern is high velocity but may be legitimate business activity |
| TC05 | C005 | B005 | Alert | 3 identical-value transactions with 3-minute gaps |
| TC06 | C006 | B006 | Alert | 3 rapid transactions crossing midnight within the 30-minute window |
| TC07 | C007 | B007 | No alert | The 09:30 transaction sits exactly on the 30-minute boundary and is included, but the 09:33 and 09:36 transactions are outside the 30-minute window, so no 3-transaction sequence exists |
| TC08 | C008 | B008 | No alert | Transaction before beneficiary creation is excluded; remaining transactions have gaps greater than 3 minutes |
| TC09 | C009 | B009 | Alert | 3 rapid transactions to B009 |
| TC10 | C009 | B010 | No alert | Same customer but only 2 transactions to B010; tests customer-beneficiary partitioning |
| TC11 | C010 | B011 | No alert | 3 transactions occur in the 30-minute window, but gaps are 15 and 9 minutes |

## Expected alert set

The rule should produce investigation alerts for:

- C001 → B001
- C003 → B003
- C004 → B004
- C005 → B005
- C006 → B006
- C009 → B009

## False-positive lesson

TC04 is intentionally included as a false-positive candidate. The velocity rule should flag it, but the investigator should not label it fraud without corroborating evidence such as device, authentication, customer history, beneficiary context, or business-purpose information.

## Edge cases covered

- Exactly 30-minute boundary
- Transactions before beneficiary creation
- Midnight date crossover
- Multiple beneficiaries belonging to the same customer
- Rapid versus slow transaction sequences
- Legitimate-looking high-volume behaviour
