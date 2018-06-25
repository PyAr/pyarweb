FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code:$PYTHONPATH

RUN mkdir /code
WORKDIR /code
COPY prod_requirements.txt /code
COPY requirements.txt /code
RUN pip install -r prod_requirements.txt
COPY . /code/
