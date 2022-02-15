#!/bin/sh

python manage.py migrate
#phython add_data_from_json
#python manage.py search_index --rebuild -f
python manage.py runserver 0.0.0.0:8000
