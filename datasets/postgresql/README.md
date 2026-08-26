# PostgreSQL Practice Dataset

Synthetic banking/fintech data for the Fraud Investigation & Transaction Risk Analytics project.

## Tables

- `customers` — customer profile and account opening data
- `accounts` — account balances/status
- `beneficiaries` — beneficiary creation history
- `transactions` — transaction-level activity
- `devices` — known device/IP information
- `login_events` — login/authentication activity

## Dataset size

- 200 customers
- 200 accounts
- 411 beneficiaries
- 2,342 transactions
- 400 devices
- 1,004 login events
- 11 planted test scenarios

## Planted scenarios

The generator deliberately includes rapid beneficiary-transfer bursts, slow sequences, a legitimate-looking false-positive candidate, repeated identical amounts, midnight crossover, an exact 30-minute boundary case, transactions before beneficiary creation, multiple beneficiaries for one customer, and new-device login events.

## Run locally

1. Install PostgreSQL and create a database such as `fraud_analytics`.
2. Install Python dependencies with `pip install -r requirements.txt`.
3. Run `python generate_dataset.py` from this directory.
4. Run `schema.sql` against the database.
5. Run `load_data.sql` from this directory using `psql`.
6. Open the database in DBeaver or another SQL client.

The generated CSV files are ignored from the repository design intentionally; the generator makes the dataset reproducible instead of storing a large set of generated files in Git.

## Ground truth

`test_cases.csv` contains expected outcomes for the planted scenarios. These are synthetic labels for testing detection logic, not claims about real fraud.
