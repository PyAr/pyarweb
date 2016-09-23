#!/bin/bash
python3 manage.py migrate
python3 manage.py loaddata fixtures/initial_data.json
