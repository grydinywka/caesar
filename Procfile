web: gunicorn caesar.wsgi:application
worker1: python worker.py
worker: python --pythonpath worker worker.py
flushredis: python --pythonpath worker flushredis.py
