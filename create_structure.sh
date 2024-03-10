#!/bin/bash

# Define your project name and base directory
PROJECT_NAME="banking-application"
BASE_DIR="./$PROJECT_NAME"

# Create the base directory
mkdir -p "$BASE_DIR"

# Define the subdirectories to be created under the base directory
declare -a SUBDIRECTORIES=(
    "frontend/public"
    "frontend/src/components"
    "frontend/src/services"
    "frontend/src/pages"
    "frontend/src/hooks"
    "frontend/src/assets"
    "backend/app/models"
    "backend/app/routes"
    "backend/app/utils"
    "backend/migrations"
    "backend/tests"
    "database/migrations"
    "database/seeds"
    "docs/api"
    "docs/design"
)

# Create the subdirectories
for DIR in "${SUBDIRECTORIES[@]}"; do
    mkdir -p "$BASE_DIR/$DIR"
done

# Create placeholder files
echo "Node.js dependencies and scripts" > "$BASE_DIR/frontend/package.json"
echo "Initialize the app" > "$BASE_DIR/backend/app/__init__.py"
echo "Project overview and setup instructions" > "$BASE_DIR/README.md"
echo "Docker compose to orchestrate services (optional)" > "$BASE_DIR/docker-compose.yml"

# Output the structure
echo "Project folder structure created at $BASE_DIR"
tree "$BASE_DIR"
