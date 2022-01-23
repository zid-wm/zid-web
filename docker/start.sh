#!/bin/bash

cd /app || exit 1

if [ "$DJANGO_DEBUG" = "true" ]; then
  gunicorn \
    --reload \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --worker-class eventlet \
    --log-level DEBUG \
    --access-logfile "-" \
    --error-logfile "-" \
    zid_web.wsgi
else
  gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --worker-class eventlet \
    --log-level DEBUG \
    --access-logfile "-" \
    --error-logfile "-" \
    zid_web.wsgi
fi