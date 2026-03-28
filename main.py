import os
from flask import Flask, jsonify
from torrequest import TorRequest

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "running"})

@app.route("/ip")
def get_ip():
    with TorRequest(proxy_port=9050, ctrl_port=9051) as tr:
        return tr.get("http://httpbin.org/ip").text

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "endpoint not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # 🔥 penting
    app.run(host="0.0.0.0", port=port)
