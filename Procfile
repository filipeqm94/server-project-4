release: python manage.py migrate
web: daphne chatter_project.asgi:application --port $PORT --bind 0.0.0.0 -v2