#!/bin/bash

set -e  # Exit when any commands fail

echo "App boot..."

# Custom shutdown signals...
# GUNICORN - graceful shutdown == TERM
killApp() {
    echo "Shutdown app processes..."
    [[ -n "$GUNICORN" ]] && kill -TERM ${GUNICORN}
    wait
}
trap killApp EXIT

# workdir
export HOME=/app USER=app
cd $HOME

# ------------------------------------------------------------------
# Sync the container "static_root" dir to the host mount (for NginX)
# ------------------------------------------------------------------
if [[ -d /app/static ]]; then
    echo "Sync static media to host mount..."
    rsync -r /app/static_root/ /app/static/
fi

# ------------------------------------------------------------------
# Run DB migrations, create initial admin user, etc.
# ------------------------------------------------------------------
echo "Django app setup (db migrate)..."
gosu app:app python /app/instance/app_setup.py


# --------------------------------------------------------------
# Start web server and task consumer
# --------------------------------------------------------------
echo "Start server processes..."

# Gunicorn WSGI server
gosu app:app gunicorn project.wsgi -c /app/instance/gunconf.py &
GUNICORN=$!

# Wait for server processes to finish
wait
