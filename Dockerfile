FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"

# Set the working directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY r.txt /code/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r r.txt

# Copy the project files
COPY . /code/

# Migrate the database
RUN python manage.py migrate
