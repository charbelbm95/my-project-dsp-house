# Use the official Airflow image as a base
FROM apache/airflow:2.1.0

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command (can be overridden by docker-compose)
CMD ["airflow", "webserver"]
