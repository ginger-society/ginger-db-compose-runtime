#!/bin/bash

set -e

echo "Starting application..."

export DJANGO_SETTINGS_MODULE=server.settings

gunicorn server.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 1 \
  --threads 2 \
  --worker-class sync \
  --timeout 60