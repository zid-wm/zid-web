#!/usr/bin/env bash

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
  (cd zid-web || return; python manage.py createsuperuser --no-input)
fi
(cd zid-web || return; gunicorn zid_web.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) & nginx -g "daemon off;"