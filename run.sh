cd web_base
rm -rf db.sqlite3
python3 manage.py migrate --run-syncdb
python3 manage.py createsuperuser --username aamet --email coolboy19521@gmail.com
python3 manage.py runserver 0.0.0.0:8000