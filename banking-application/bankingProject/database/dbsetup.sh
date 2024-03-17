#!/bin/bash
#bash dbsetup.sh
# Define variables
DB_NAME="banking_app"
SQL_FILE="schema.sql"

# Create the database
createdb -U postgres "$DB_NAME"

# Check if database creation was successful
if [ $? -eq 0 ]; then
    echo "Database '$DB_NAME' created successfully"
else
    echo "Failed to create database '$DB_NAME'"
    exit 1
fi

# Run the schema script
psql -U postgres -d "$DB_NAME" -a -f "$SQL_FILE"

# Check if schema script execution was successful
if [ $? -eq 0 ]; then
    echo "Schema script '$SQL_FILE' executed successfully"
else
    echo "Failed to execute schema script '$SQL_FILE'"
    exit 1
fi

echo "Setup completed successfully"
