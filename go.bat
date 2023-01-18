@ECHO OFF
pip install -r requirements.txt
cd gatekeeper_backend
python manage.py runserver