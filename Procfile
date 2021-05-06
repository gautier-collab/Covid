web: python manage.py collectstatic --no-input; gunicorn project.wsgi --log-file - --log-level debug
worker: python manage.py scrape 06 00