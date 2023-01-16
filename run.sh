#!/bin/bash
# Let's call this script venv.sh
source "env1/bin/activate"
pip install -r requirements.txt
cd gatekeeper_backend
python3 manage.py runserver