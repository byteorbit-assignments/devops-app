from os import getenv

bind = '0.0.0.0:8080'
max_requests = 5000

worker_class = getenv('WSGI_WORKER_CLASS', 'gevent')
workers = int(getenv('WSGI_WORKERS', '2'))

def post_fork(server, worker):
    # Apply gevent monkey patches...
    # Gunicorn already does "gevent.monkey.patch_all()"
    # We only need to patch psycopg2 (PostgreSQL db driver)
    if worker.__class__.__name__ == 'GeventWorker':
        server.log.info('... psycogreen')
        from psycogreen import gevent
        gevent.patch_psycopg()
