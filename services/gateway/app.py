from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
import requests
from datetime import datetime
import json

app = Flask(__name__, template_folder='templates', static_folder='static')

# Config via ConfigMap/Secret
APP_NAME = os.environ.get("APP_NAME", "Travel Mini")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme")

FLIGHTS_SVC = os.environ.get("FLIGHTS_SVC", "flights")
HOTELS_SVC = os.environ.get("HOTELS_SVC", "hotels")

FLIGHTS_URL = f"http://{FLIGHTS_SVC}:5000"
HOTELS_URL = f"http://{HOTELS_SVC}:5000"

# Homepage
@app.route("/")
def index():
    return render_template("index.html", app_name=APP_NAME)

# Combined listings page: get flights and hotels and show them
@app.route("/listings")
def listings():
    flights = []
    hotels = []
    try:
        r = requests.get(f"{FLIGHTS_URL}/api/flights", timeout=2)
        flights = r.json() if r.status_code == 200 else []
    except Exception:
        flights = []
    try:
        r = requests.get(f"{HOTELS_URL}/api/hotels", timeout=2)
        hotels = r.json() if r.status_code == 200 else []
    except Exception:
        hotels = []
    return render_template("listings.html", flights=flights, hotels=hotels)

# API passthrough for flights/hotels (optional)
@app.route("/api/flights")
def api_flights():
    try:
        r = requests.get(f"{FLIGHTS_URL}/api/flights", timeout=2)
        return jsonify(r.json()), r.status_code
    except Exception:
        return jsonify([]), 503

@app.route("/api/hotels")
def api_hotels():
    try:
        r = requests.get(f"{HOTELS_URL}/api/hotels", timeout=2)
        return jsonify(r.json()), r.status_code
    except Exception:
        return jsonify([]), 503

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/readyz")
def readyz():
    return "ready", 200

# Simple admin endpoint (protected by query param pw for demo)
@app.route("/admin")
def admin():
    pw = request.args.get("pw")
    if pw != ADMIN_PASSWORD:
        return "Unauthorized", 401
    return jsonify({"app": APP_NAME, "time": datetime.utcnow().isoformat() + "Z"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
