web: gunicorn Wao.asgi -k uvicorn.workers.UvicornWorker --timeout 120 --workers=3 --preload
web2: daphne Wao.asgi:wmoviestest --port $PORT --bind 0.0.0.0 
worker: python manage.py runworker -v2

