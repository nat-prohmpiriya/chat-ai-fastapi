#!/bin/bash
set -e

# Load environment variables
source .env

# Start Gunicorn with config
pipenv run gunicorn src.main:app \
    --config gunicorn.conf.py \
    --access-logfile - \
    --error-logfile - \
    --log-level info