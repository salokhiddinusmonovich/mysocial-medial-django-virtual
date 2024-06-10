FROM python:3.10-slim

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r r.txt

# Install uWSGI
RUN pip install uwsgi

# Copy the project files
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput
