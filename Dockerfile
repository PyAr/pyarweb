FROM python:3.4
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code:$PYTHONPATH
# runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \ 
    zlib1g-dev \
    libffi-dev \ 
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code
# update pip (to use wheels)
RUN wget -O - https://bootstrap.pypa.io/get-pip.py | python3
COPY dev_requirements.txt /code
COPY requirements.txt /code
RUN pip install -r dev_requirements.txt
COPY . /code/
