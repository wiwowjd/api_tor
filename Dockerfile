FROM python:3.10-slim

# Install Tor + netcat
RUN apt-get update && \
    apt-get install -y tor netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Copy tor config
COPY torrc /etc/tor/torrc

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App
WORKDIR /app
COPY . .

# Script
COPY wait-for-tor.sh /wait-for-tor.sh
RUN chmod +x /wait-for-tor.sh

CMD ["/wait-for-tor.sh"]
