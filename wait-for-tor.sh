#!/bin/bash

# Start Tor di background
tor &

echo "Waiting for Tor to fully bootstrap (SocksPort 9050)..."

# Loop sampai port 9050 terbuka
while ! nc -z 127.0.0.1 9050; do
  sleep 1
done

echo "Tor is ready! Starting Gunicorn..."

# Jalankan Flask/Gunicorn di PID1 supaya container tetap hidup
exec gunicorn -b 0.0.0.0:$PORT main:app
