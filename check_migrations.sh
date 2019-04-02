#!/bin/bash 

# This script will return exit 1 if pending migrations exists.

python3 ./manage.py makemigrations --dry-run -e
if [ $? -ne 1 ]; then
       echo "Pending migrations!!"
       exit 1
fi 
exit 0
