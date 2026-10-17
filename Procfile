release: python manage.py migrate --noinput && python manage.py seed_catalog --update
web: gunicorn maternabox.wsgi --log-file -
