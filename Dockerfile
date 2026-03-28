FROM python:3.10-slim

# Install Tor
RUN apt-get update && apt-get install -y tor curl && rm -rf /var/lib/apt/lists/*

# Copy config tor
COPY torrc /etc/tor/torrc

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
WORKDIR /app
COPY . .

# Expose port (optional kalau pakai API)
EXPOSE 8000

# Start Tor + App
CMD tor & sleep 5 && python main.py
