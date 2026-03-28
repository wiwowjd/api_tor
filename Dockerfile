FROM python:3.10-slim

RUN apt-get update && apt-get install -y tor && rm -rf /var/lib/apt/lists/*

COPY torrc /etc/tor/torrc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . .

# 🔥 Gunicorn (lebih stabil di Railway)
CMD tor & sleep 5 && gunicorn -b 0.0.0.0:$PORT main:app
