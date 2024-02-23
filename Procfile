pip install gunicorn
web: gunicorn baun_media.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate