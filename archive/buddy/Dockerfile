FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .

RUN set -ex \
  && apt update \
  && apt install -y \
    gcc tar build-essential

COPY . /app/

# Installing ta-lib
RUN set -ex \
  && tar -xzf /app/bin/ta-lib-0.4.0-src.tar.gz \
  && cd ta-lib/ \
  && ./configure --prefix=/usr \
  && make && make install \
  && cd ..

# Installing python dependencies
RUN set -ex \
  && pip install -r requirements.txt

# EXPOSE 8000
# CMD python manage.py runserver 0.0.0.0:8000