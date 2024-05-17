#!/bin/bash
# Initialize the database
airflow db init

# Create an admin user if it doesn't already exist
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Execute the CMD from the Dockerfile or docker-compose.yml
exec "$@"
