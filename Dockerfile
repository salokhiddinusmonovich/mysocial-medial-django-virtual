FROM python:3.10-slim-bullseye



WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY r.txt .

RUN pip install -r r.txt
RUN apt-get update && apt-get install -y build-essential



COPY . .


