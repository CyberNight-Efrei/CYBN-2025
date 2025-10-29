#!/bin/sh

python3 db_init.py

gunicorn -w 4 "app:app" -b 0.0.0.0:8000 -t 0