-- Create a new schema
CREATE SCHEMA retail_banking;

-- Create customer Table under the new schema
CREATE TABLE retail_banking.customer (
    customer_id SERIAL PRIMARY KEY,
    customername VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    created_by INT,
    updated_by INT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES retail_banking.customer(customer_id),
    FOREIGN KEY (updated_by) REFERENCES retail_banking.customer(customer_id)
);

-- Create Session Table under the new schema
CREATE TABLE retail_banking.Session (
    session_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES retail_banking.customer(customer_id) ON DELETE CASCADE,
    token VARCHAR(64) UNIQUE NOT NULL,
    expiry_timestamp TIMESTAMP NOT NULL,
    created_by INT,
    updated_by INT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES retail_banking.customer(customer_id),
    FOREIGN KEY (updated_by) REFERENCES retail_banking.customer(customer_id)
);

-- Create AccountType Table under the new schema
CREATE TABLE retail_banking.AccountType (
    account_type_id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL
);

-- Populate AccountType Table with initial data
INSERT INTO retail_banking.AccountType (name) VALUES
('Savings'),
('Checking'),
('Investment'),
('Loan');

-- Create Account Table under the new schema
CREATE TABLE retail_banking.Account (
    account_id SERIAL PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id INT REFERENCES retail_banking.customer(customer_id) ON DELETE CASCADE,
    balance DECIMAL(20, 2) DEFAULT 0,
    account_type_id INT REFERENCES retail_banking.AccountType(account_type_id),
    account_description VARCHAR(1000),
    created_by INT,
    updated_by INT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES retail_banking.customer(customer_id),
    FOREIGN KEY (updated_by) REFERENCES retail_banking.customer(customer_id)
);

-- Create Transaction Table under the new schema
CREATE TABLE retail_banking.Transaction (
    transaction_id SERIAL PRIMARY KEY,
    transaction_type VARCHAR(20),
    amount DECIMAL(20, 2),
    source_account_id INT REFERENCES retail_banking.Account(account_id) ON DELETE CASCADE,
    destination_account_id INT REFERENCES retail_banking.Account(account_id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES retail_banking.customer(customer_id),
    FOREIGN KEY (updated_by) REFERENCES retail_banking.customer(customer_id)
);
