-- Create a new schema
CREATE SCHEMA retail_banking;

-- Create User Table under the new schema
CREATE TABLE retail_banking."User" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    created_by INT,
    updated_by INT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES retail_banking."User"(user_id),
    FOREIGN KEY (updated_by) REFERENCES retail_banking."User"(user_id)
);

-- Create Session Table under the new schema
CREATE TABLE retail_banking.Session (
    session_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES retail_banking."User"(user_id) ON DELETE CASCADE,
    token VARCHAR(64) UNIQUE NOT NULL,
    expiry_timestamp TIMESTAMP NOT NULL,
    created_by INT,
    updated_by INT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES retail_banking."User"(user_id),
    FOREIGN KEY (updated_by) REFERENCES retail_banking."User"(user_id)
);

-- Create Account Table under the new schema
CREATE TABLE retail_banking.Account (
    account_id SERIAL PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    user_id INT REFERENCES retail_banking."User"(user_id) ON DELETE CASCADE,
    balance DECIMAL(20, 2) DEFAULT 0,
    account_type VARCHAR(20),
    created_by INT,
    updated_by INT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES retail_banking."User"(user_id),
    FOREIGN KEY (updated_by) REFERENCES retail_banking."User"(user_id)
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
    FOREIGN KEY (created_by) REFERENCES retail_banking."User"(user_id),
    FOREIGN KEY (updated_by) REFERENCES retail_banking."User"(user_id)
);
