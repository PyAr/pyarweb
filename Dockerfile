FROM ubuntu:14.04

ENV PYTHONUNBUFFERED 1

RUN apt-get -qq update && apt-get install -y  --no-install-recommends \
    build-essential \
    git \
    python3 \
    python3-dev \
    gettext \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng12-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code

ADD . /code/
RUN pip3 install -U pip setuptools
RUN pip3 install -r requirements.txt
