ARG py=3.7

# --------------------------------------------------------------------
# Build stage 1 -- VENV
# --------------------------------------------------------------------
FROM byteorbit/py-base:$py as venv

# Pip install server libs - install these first (for docker cache)
RUN pip install --no-cache-dir \
    gunicorn~=19.9.0 gevent~=1.4.0 \
    psycopg2~=2.8.0 psycogreen \
    redlock~=1.2.0 \
    dumb-init~=1.2.0

# Pip install libs.
COPY . /app/src/
RUN pip install --no-cache-dir -r /app/src/requirements/base.txt

# Install project
RUN pip install -e /app/src/

# --------------------------------------------------------------------
# Build stage 2 -- STATIC_ROOT
# Allows us to exclude node and node_modules from final stage
# --------------------------------------------------------------------
FROM byteorbit/py-build:$py as static

ENV DJANGO_SETTINGS_MODULE='project.settings' \
    STATIC_ROOT="/app/static_root"

# Workdir for output to /app/node_modules
WORKDIR /app

COPY --from=venv /app/src /app/src
COPY --from=venv /venv /venv
RUN /app/src/manage.py collectstatic --noinput --verbosity 0

# --------------------------------------------------------------------
# Final stage
# --------------------------------------------------------------------
FROM venv

# Minimal env required for boot...
ENV DJANGO_SETTINGS_MODULE='project.settings' \
    BASE_DIR="/app/instance" \
    STATIC_ROOT="/app/static_root" \
    DATA_DIR="/app/data"


# Copy static files
COPY --from=static $STATIC_ROOT $STATIC_ROOT

# Copy deploy conf dir
ADD --chown=app:app deploy_conf $BASE_DIR

# App boot...
USER root
EXPOSE 8080
ADD boot.sh /app/boot.sh
RUN chmod +x /app/boot.sh
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/app/boot.sh"]
