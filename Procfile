web: gunicorn Wao.asgi:application -k uvicorn.workers.UvicornWorker --timeout 120 --workers=3 --preload
web2: daphne Wao.asgi:application --port $PORT --bind 0.0.0.0 
worker: python manage.py runworker -v2

