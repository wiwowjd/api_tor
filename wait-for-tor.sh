#!/bin/bash

# Start Tor
tor &

echo "Waiting for Tor (9050)..."

# Tunggu sampai port 9050 kebuka
while ! nc -z 127.0.0.1 9050; do
  sleep 1
done

echo "Tor ready! Starting Gunicorn..."

exec gunicorn -b 0.0.0.0:$PORT main:app
