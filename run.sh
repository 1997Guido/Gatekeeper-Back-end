#!/bin/bash
# Let's call this script venv.sh
source "env1/bin/activate"
cd gatekeeper_backend
python3 manage.py runserver