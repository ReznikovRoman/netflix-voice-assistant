#!/bin/sh

gunicorn --worker-class uvicorn.workers.UvicornWorker \
  --workers 2 \
  --bind 0.0.0.0:$NVA_SERVER_PORT \
  voice_assistant.main:create_app

# Run the main container process
exec "$@"
