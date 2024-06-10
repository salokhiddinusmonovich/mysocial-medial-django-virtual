FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
RUN mkdir /code
WORKDIR /code
COPY r.txt .

RUN pip install --upgrade pip
RUN pip install -r r.txt
COPY . .
RUN python manage.py migrate
