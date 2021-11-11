FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .

RUN set -ex \
  && apt update \
  && apt install -y \
    gcc \
  && pip install -r requirements.txt

COPY . /app/
# EXPOSE 8000
# CMD python manage.py runserver 0.0.0.0:8000