# Use the official Python image as a base
FROM python:3.8
# FROM python:3.8-slim-buster

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# sudo apt install build-essential

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update \
    && apt-get install -y \
    libpq-dev \
    postgresql-client
    
# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install Redis server
RUN apt-get update && apt-get install -y redis-server

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Start Redis and Django application
CMD ["sh", "-c", "redis-server --daemonize yes && daphne -b 0.0.0.0 -p 8000 dermepro.asgi:application"]
