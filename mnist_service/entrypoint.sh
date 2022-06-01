#!/usr/bin/env bash

sleep 20
flask db init
flask db upgrade
gunicorn -b 0.0.0.0:8000 run:app --timeout 600
