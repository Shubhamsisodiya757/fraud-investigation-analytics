DROP TABLE IF EXISTS login_events;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS beneficiaries;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100),
    occupation VARCHAR(100),
    account_open_date DATE
);

CREATE TABLE accounts (
    account_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) REFERENCES customers(customer_id),
    balance NUMERIC(18,2),
    status VARCHAR(20)
);

CREATE TABLE devices (
    customer_id VARCHAR(20) REFERENCES customers(customer_id),
    device_id VARCHAR(50) PRIMARY KEY,
    ip_address VARCHAR(50),
    device_type VARCHAR(50),
    login_city VARCHAR(100),
    first_seen TIMESTAMP
);

CREATE TABLE beneficiaries (
    customer_id VARCHAR(20) REFERENCES customers(customer_id),
    beneficiary_account VARCHAR(50) PRIMARY KEY,
    added_on TIMESTAMP,
    verified BOOLEAN,
    bank_name VARCHAR(50)
);

CREATE TABLE transactions (
    txn_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) REFERENCES customers(customer_id),
    from_account VARCHAR(20) REFERENCES accounts(account_id),
    to_account VARCHAR(50),
    amount NUMERIC(18,2),
    txn_time TIMESTAMP,
    channel VARCHAR(30),
    status VARCHAR(20)
);

CREATE TABLE login_events (
    login_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) REFERENCES customers(customer_id),
    device_id VARCHAR(50),
    ip_address VARCHAR(50),
    login_time TIMESTAMP,
    login_city VARCHAR(100)
);

CREATE INDEX idx_txn_customer_time ON transactions(customer_id, txn_time);
CREATE INDEX idx_txn_to_account_time ON transactions(to_account, txn_time);
CREATE INDEX idx_beneficiary_customer_added ON beneficiaries(customer_id, added_on);
CREATE INDEX idx_login_customer_time ON login_events(customer_id, login_time);
