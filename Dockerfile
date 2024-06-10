FROM python:3.6-stretch
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
RUN mkdir /code
WORKDIR /code
COPY r.txt .
RUN pip install -r r.txt
ADD . .
#RUN python manage.py migrate