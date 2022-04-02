release: python3 manage.py makemigrations && python3 manage.py migrate
web: daphne core.asgi.application --port $PORT --bind 0.0.0.0 -v2
worker: python3 manage.py runworker channel_layer -v2