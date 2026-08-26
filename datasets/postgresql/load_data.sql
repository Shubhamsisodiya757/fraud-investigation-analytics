-- Run from datasets/postgresql with psql after creating a database such as fraud_analytics.
-- Example:
-- psql -d fraud_analytics -f schema.sql
-- psql -d fraud_analytics -f load_data.sql

\copy customers FROM 'data/customers.csv' CSV HEADER;
\copy accounts FROM 'data/accounts.csv' CSV HEADER;
\copy devices FROM 'data/devices.csv' CSV HEADER;
\copy beneficiaries FROM 'data/beneficiaries.csv' CSV HEADER;
\copy transactions FROM 'data/transactions.csv' CSV HEADER;
\copy login_events FROM 'data/login_events.csv' CSV HEADER;
