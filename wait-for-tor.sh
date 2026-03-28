#!/bin/bash
# Start Tor in background
tor &

# Wait until Tor is bootstrapped
echo "Waiting for Tor to boot..."
while ! nc -z 127.0.0.1 9050; do
  sleep 1
done

# Start Gunicorn
exec gunicorn -b 0.0.0.0:$PORT main:app
