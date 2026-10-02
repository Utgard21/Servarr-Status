import os
import time
import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

SERVICES = {
    "sonarr": {
        "name": "Sonarr",
        "url": os.getenv("SONARR_URL", "").rstrip("/"),
        "api_key": os.getenv("SONARR_API_KEY", ""),
        "endpoint": "/api/v3/system/status",
    },
    "radarr": {
        "name": "Radarr",
        "url": os.getenv("RADARR_URL", "").rstrip("/"),
        "api_key": os.getenv("RADARR_API_KEY", ""),
        "endpoint": "/api/v3/system/status",
    },
}

def check_service(service):
    started = time.perf_counter()
    if not service["url"]:
        return {"status": "not_configured", "error": "URL not configured"}

    try:
        r = requests.get(
            service["url"] + service["endpoint"],
            headers={"X-Api-Key": service["api_key"]},
            timeout=5,
        )
        ms = round((time.perf_counter() - started) * 1000)
        if r.ok:
            data = r.json()
            return {
                "status": "online",
                "response_ms": ms,
                "version": data.get("version", "unknown"),
                "branch": data.get("branch", ""),
            }
        return {
            "status": "offline",
            "response_ms": ms,
            "error": f"HTTP {r.status_code}",
        }
    except requests.RequestException as e:
        return {"status": "offline", "error": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    result = {}
    for key, service in SERVICES.items():
        result[key] = {"name": service["name"], **check_service(service)}
    return jsonify({"timestamp": int(time.time()), "services": result})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
