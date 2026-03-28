FROM python:3.10-slim

# Install Tor + netcat (nc)
RUN apt-get update && \
    apt-get install -y tor netcat-openbsd curl && \
    rm -rf /var/lib/apt/lists/*

# Copy tor configuration
COPY torrc /etc/tor/torrc

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
WORKDIR /app
COPY . .

# Copy wait-for-tor script
COPY wait-for-tor.sh /wait-for-tor.sh
RUN chmod +x /wait-for-tor.sh

# Start container
CMD ["/wait-for-tor.sh"]
