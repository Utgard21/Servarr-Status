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
        "kind": "servarr",
    },
    "radarr": {
        "name": "Radarr",
        "url": os.getenv("RADARR_URL", "").rstrip("/"),
        "api_key": os.getenv("RADARR_API_KEY", ""),
        "kind": "servarr",
    },
    "bazarr": {
        "name": "Bazarr",
        "url": os.getenv("BAZARR_URL", "").rstrip("/"),
        "api_key": os.getenv("BAZARR_API_KEY", ""),
        "kind": "bazarr",
    },
    "fetcharr": {
        "name": "Fetcharr",
        "url": os.getenv("FETCHARR_URL", "").rstrip("/"),
        "kind": "generic",
    },
    "flaresolverr": {
        "name": "FlareSolverr",
        "url": os.getenv("FLARESOLVERR_URL", "").rstrip("/"),
        "kind": "flaresolverr",
    },
    "jackett": {
        "name": "Jackett",
        "url": os.getenv("JACKETT_URL", "").rstrip("/"),
        "api_key": os.getenv("JACKETT_API_KEY", ""),
        "kind": "jackett",
    },
    "plungarr": {
        "name": "Plungarr",
        "url": os.getenv("PLUNGARR_URL", "").rstrip("/"),
        "kind": "generic",
    },
}

TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "5"))

def request(url, headers=None, params=None):
    started = time.perf_counter()
    response = requests.get(url, headers=headers or {}, params=params or {}, timeout=TIMEOUT)
    ms = round((time.perf_counter() - started) * 1000)
    return response, ms

def check_service(service):
    if not service["url"]:
        return {"status": "not_configured", "error": "URL not configured"}

    try:
        kind = service["kind"]
        if kind == "servarr":
            r, ms = request(
                service["url"] + "/api/v3/system/status",
                headers={"X-Api-Key": service.get("api_key", "")},
            )
            if r.ok:
                data = r.json()
                return {
                    "status": "online",
                    "response_ms": ms,
                    "version": data.get("version", "unknown"),
                }

        elif kind == "bazarr":
            headers = {"X-API-KEY": service.get("api_key", "")} if service.get("api_key") else {}
            r, ms = request(service["url"] + "/api/system/ping", headers=headers)
            if r.ok:
                return {"status": "online", "response_ms": ms, "version": "reachable"}

        elif kind == "flaresolverr":
            r, ms = request(service["url"] + "/health")
            if r.ok:
                version = "reachable"
                try:
                    payload = r.json()
                    version = payload.get("version") or payload.get("msg") or version
                except ValueError:
                    pass
                return {"status": "online", "response_ms": ms, "version": version}

        elif kind == "jackett":
            params = {"apikey": service.get("api_key", "")} if service.get("api_key") else {}
            r, ms = request(service["url"] + "/api/v2.0/server/config", params=params)
            if r.ok:
                version = "reachable"
                try:
                    payload = r.json()
                    version = payload.get("app_version") or payload.get("appVersion") or version
                except ValueError:
                    pass
                return {"status": "online", "response_ms": ms, "version": version}

        else:
            r, ms = request(service["url"])
            if r.status_code < 500:
                return {"status": "online", "response_ms": ms, "version": "reachable"}

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
