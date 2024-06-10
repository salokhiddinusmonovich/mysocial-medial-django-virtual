FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"

# Create and set working directory
RUN mkdir /code
WORKDIR /code

# Copy the requirements file and install dependencies
COPY r.txt .
RUN pip install --upgrade pip
RUN pip install -r r.txt

# Copy the Django project files into the container
COPY . .

# Install uwsgi
RUN pip install uwsgi

# Run Django migrations
# RUN python manage.py migrate

# Command to start uwsgi server
CMD ["uwsgi", "--socket=:9000", "--module=a_core.wsgi:application", "--py-autoreload=1"]
