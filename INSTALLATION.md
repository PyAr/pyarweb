# Installation Notes

## Prerequisites

Make sure you have installed...

```bash
sudo apt-get install python3-dev libxml2-dev libxslt1-dev zlib1g-dev libffi-dev openssl-dev
```

## Create virtualenv

You should use virtualenv (or [FADES](https://github.com/PyAr/fades)). Currently supports 3.5.
Create a virtualenv named `pyarweb`

### Pyenv

```bash
pyvenv3 pyarweb
```

### Virtualenvwrapper

If you don't know how to use `virtualenvwrapper` please check [official documentation](https://virtualenvwrapper.readthedocs.io/en/latest/)

```bash
mkvirtualenv -p $(which python3) pyarweb
```

## Install requirements

```bash
pip install -r dev_requirements.txt
```

## Create PostgresSQL DB

### with Docker engine

```bash
docker run --name pyarweb-db -e POSTGRES_DB=pyarweb -p 5432:5432 -d postgres
```

### with PostgreSQL

```bash
su - postgres
createdb pyarweb
```

## Initialize DB

```bash
./manage.py makemigrations  # because Waliki presents some bug...
./manage.py migrate
```

## Run some test
```bash
./manage.py test
```

# Run service

```bash
./manage.py runserver
```