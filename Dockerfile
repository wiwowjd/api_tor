FROM python:3.10-slim

# Install Tor
RUN apt-get update && \
    apt-get install -y tor && \
    rm -rf /var/lib/apt/lists/*

# Copy tor config
COPY torrc /etc/tor/torrc

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
WORKDIR /app
COPY . .

# Run Tor + Gunicorn
# ⚡ wait-for-tor.sh memastikan Tor fully bootstrapped sebelum Gunicorn jalan
COPY wait-for-tor.sh /wait-for-tor.sh
RUN chmod +x /wait-for-tor.sh

CMD ["/wait-for-tor.sh"]
