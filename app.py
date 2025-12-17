import os
import socket
import requests
import urllib3

from flask import Flask, render_template, request, jsonify
from netaddr import valid_ipv4, valid_ipv6

# -----------------------------------------------------------------------------
# App setup
# -----------------------------------------------------------------------------
app = Flask(__name__)

# -----------------------------------------------------------------------------
# Config (from Docker / env)
# -----------------------------------------------------------------------------
GM_USER = os.environ.get("GM_USER")
GM_PWD = os.environ.get("GM_PWD")
GM_URL = os.environ.get("GM_URL")
WAPI_VERSION = os.environ.get("WAPI_VERSION")

if not GM_USER or not GM_PWD or not GM_URL:
    raise RuntimeError("Username (GM_USER), password (GM_PWD) and URL (GM_URL) must be set")

INFOBLOX_URL = "https://" + GM_URL + "/wapi/" + WAPI_VERSION + "/search"
REQUEST_TIMEOUT = 10

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -----------------------------------------------------------------------------
# UI route (HTML ONLY)
# -----------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("app_dns/querydns.html")

# -----------------------------------------------------------------------------
# API route (JSON ONLY)
# -----------------------------------------------------------------------------
@app.route("/api/querydns", methods=["GET"])
def api_querydns():
    ipaddress = request.args.get("ip", "").strip()

    if not ipaddress:
        return jsonify(error="IP address or hostname is required"), 400

    try:
        if not valid_ipv4(ipaddress) and not valid_ipv6(ipaddress):
            ipaddress = socket.gethostbyname(ipaddress)
    except Exception as e:
        return jsonify(error=f"DNS resolution failed: {e}"), 400

    try:
        response = requests.get(
            INFOBLOX_URL,
            params={"address": ipaddress},
            auth=(GM_USER, GM_PWD),
            verify=False,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        return jsonify(
            ip=ipaddress,
            result=response.text
        )

    except requests.exceptions.RequestException as e:
        return jsonify(error=f"Infoblox request failed: {e}"), 500


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)

