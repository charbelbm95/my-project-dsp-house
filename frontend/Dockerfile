# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install the PostgreSQL development libraries
RUN apt-get update && apt-get install -y gcc libpq-dev

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit is running on
EXPOSE 8501

# Run Streamlit server
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
