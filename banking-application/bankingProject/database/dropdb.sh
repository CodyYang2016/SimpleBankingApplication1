#!/bin/bash
#bash dropdb.sh

# Define variables
DB_USER="postgres"
DB_NAME="banking_app"

# Drop the database
dropdb -U "$DB_USER" "$DB_NAME"

# Check if database drop was successful
if [ $? -eq 0 ]; then
    echo "Database '$DB_NAME' dropped successfully"
else
    echo "Failed to drop database '$DB_NAME'"
    exit 1
fi

echo "Database drop completed successfully"
