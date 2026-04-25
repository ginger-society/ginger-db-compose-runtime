#!/bin/bash

set -e

echo "Starting application..."

export DJANGO_SETTINGS_MODULE=server.settings

uwsgi \
  --http 0.0.0.0:8000 \
  --module server.wsgi:application \
  --master \
  --processes 1 \
  --threads 1 \
  --enable-threads \
  --vacuum \
  --die-on-term \
  --buffer-size 65535 \
  --static-map /static=/app/static-dist