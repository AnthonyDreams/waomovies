web: gunicorn Wao.asgi:application -k uvicorn.workers.UvicornWorker --timeout 120 --workers=1 --preload
web2: gunicorn Wao.asgi:application
worker: python manage.py runworker -v2

