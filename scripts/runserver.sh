#!/bin/bash

echo "debug = True" > /opt/code/pyarweb/devsettings.py
chmod +x /opt/code/manage.py
cd /opt/code; ./manage.py migrate && ./manage.py runserver 0.0.0.0:8000
