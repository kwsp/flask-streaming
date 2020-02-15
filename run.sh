#!/bin/bash
#CAMERA=opencv gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:5000 app:app
CAMERA=opencv gunicorn --threads 5 --workers 1 --bind 0.0.0.0:5000 app:app
