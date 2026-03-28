import os
import time
from flask import Flask, jsonify, request
from torrequest import TorRequest
from pypasser import reCaptchaV3
app = Flask(__name__)

PORT = int(os.environ.get("PORT", 8080))

### whatsapp leak
class whatsapp:
    def __init__(self):
        self.anchor = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LcTNcMUAAAAALfLcgD0y-A5e6t4vefcFNdeH5ED&co=aHR0cHM6Ly93aGF0c2FwcC5jaGVja2xlYWtlZC5jYzo0NDM.&hl=id&v=gYdqkxiddE5aXrugNbBbKgtN&size=invisible&anchor-ms=20000&execute-ms=30000&cb=23tlkj4nz0d0"
        self.data = {}
        self.telegram = True
        self.google = True
        self.includeLeakCheckPro = True
        self.enableGeminiFaceAnalysis = True
        self.params = {}
        self.UA = "https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt"

    def Get(self,number: int) -> dict:
        bypassCaptchaV3 = reCaptchaV3(self.anchor)
        getUa = random.choice(Requs.get(self.UA).text.split("\n"))
        self.params = {
            'token': bypassCaptchaV3,
            'telegram': self.telegram,
            'google': self.google,
            'includeLeakCheckPro': self.includeLeakCheckPro,
            'enableGeminiFaceAnalysis': self.enableGeminiFaceAnalysis,
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id,en-US;q=0.9,en;q=0.8,ar;q=0.7,ru;q=0.6',
            'cache-control': 'no-cache, no-store, must-revalidate',
            'dnt': '1',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'https://whatsapp.checkleaked.cc/id/{number}',
            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sw-bypass': 'true',
            'user-agent': getUa,
        }

        try:
            proxyPort=9050
            ctrlPort=9051
            
            with TorRequest(proxy_port=proxyPort, ctrl_port=ctrlPort, password=None) as tr:
                response = tr.get(
                    f'https://whatsapp.checkleaked.cc/api/phone/{number}',
                    params=self.params,
                    cookies={
                        'lang': 'id',
                        '_ga': 'GA1.1.1944623320.1766327186',
                        'includeTelegram': 'true',
                        'includeCheckleaked': 'false',
                        'includeLeakCheckPro': 'true',
                        'includeGoogle': 'true',
                        'enableGeminiFaceAnalysis': 'true',
                        '_ga_J7TCBEVNWR': 'GS2.1.s1770611185$o3$g1$t1770611259$j56$l0$h0',
                    },
                    headers=headers
                ).json()
                
            return(response)
        except Exception as e:
            return(e)
            
# helper request via Tor
def tor_get(url, retries=3):
    for _ in range(retries):
        try:
            with TorRequest(proxy_port=9050, ctrl_port=9051) as tr:
                return tr.get(url, timeout=20)
        except Exception as e:
            time.sleep(2)
    return None

# =========================
# ROOT
# =========================
@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "service": "Tor API",
        "endpoints": ["/ip", "/ip-detail", "/new-ip"]
    })

# =========================
# GET IP (simple)
# =========================
@app.route("/ip")
def get_ip():
    res = tor_get("http://httpbin.org/ip")
    
    if not res:
        return jsonify({"status": "error", "message": "Tor request failed"}), 500

    return jsonify({
        "status": "success",
        "data": res.json()
    })

# =========================
# GET FULL IP INFO
# =========================
@app.route("/ip-detail")
def ip_detail():
    # pakai ip-api (lebih lengkap)
    res = tor_get("http://ip-api.com/json/")
    
    if not res:
        return jsonify({"status": "error", "message": "Tor request failed"}), 500

    data = res.json()

    return jsonify({
        "status": "success",
        "data": {
            "ip": data.get("query"),
            "country": data.get("country"),
            "country_code": data.get("countryCode"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "zip": data.get("zip"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "timezone": data.get("timezone"),
            "isp": data.get("isp"),
            "org": data.get("org"),
            "as": data.get("as")
        }
    })

# =========================
# NEW IP (rotate Tor)
# =========================
@app.route("/new-ip")
def new_ip():
    try:
        with TorRequest(proxy_port=9050, ctrl_port=9051) as tr:
            tr.reset_identity()
            time.sleep(3)  # kasih waktu rotate

            res = tr.get("http://httpbin.org/ip")

            return jsonify({
                "status": "success",
                "new_ip": res.json()
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =========================
# CUSTOM FETCH (optional 🔥)
# =========================
@app.route("/fetch")
def fetch():
    url = request.args.get("url")

    if not url:
        return jsonify({"status": "error", "message": "url param required"}), 400

    res = tor_get(url)

    if not res:
        return jsonify({"status": "error", "message": "failed fetch"}), 500

    return jsonify({
        "status": "success",
        "url": url,
        "content_length": len(res.text)
    })

@app.route("/phone-check")
def phone_check():
    number = request.args.get("number")

    if not number:
        return jsonify({
            "status": "error",
            "message": "number param required"
        }), 400

    checker = whatsapp()
    result = checker.Get(int(number))

    return jsonify({
        "status": "success",
        "number": number,
        "result": result
    })
# =========================
# 404 HANDLER
# =========================
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "error",
        "message": "endpoint not found"
    }), 404

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
