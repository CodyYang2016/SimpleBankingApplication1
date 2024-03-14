-- Drop all tables in the schema
DROP TABLE IF EXISTS retail_banking.Transaction;
DROP TABLE IF EXISTS retail_banking.Account;
DROP TABLE IF EXISTS retail_banking.Session;
DROP TABLE IF EXISTS retail_banking."User";
DROP TABLE IF EXISTS retail_banking.AccountType;

-- Drop the schema
DROP SCHEMA IF EXISTS retail_banking CASCADE;
