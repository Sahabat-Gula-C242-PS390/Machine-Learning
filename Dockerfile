# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Ensure the src directory and models are in the correct location
COPY src /app/src
COPY src/models /app/src/models

# Make port 5000 available (common for Flask applications)
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the main application
CMD ["python", "src/main.py"]