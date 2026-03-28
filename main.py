from flask import Flask, jsonify
from torrequest import TorRequest

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "running"})

@app.route("/ip")
def get_ip():
    try:
        with TorRequest(proxy_port=9050, ctrl_port=9051) as tr:
            res = tr.get("http://httpbin.org/ip")
            return jsonify({"ip": res.json()})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/new-ip")
def new_ip():
    try:
        with TorRequest(proxy_port=9050, ctrl_port=9051) as tr:
            tr.reset_identity()
            res = tr.get("http://httpbin.org/ip")
            return jsonify({"new_ip": res.json()})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "endpoint not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
