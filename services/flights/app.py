from flask import Flask, jsonify
app = Flask(__name__)

FLIGHTS = [
    {"id": 1, "from": "NYC", "to": "LAX", "price": 150, "depart": "2025-09-01"},
    {"id": 2, "from": "SFO", "to": "SEA", "price": 90, "depart": "2025-09-10"},
    {"id": 3, "from": "NYC", "to": "BOS", "price": 60, "depart": "2025-11-03"}
]

@app.route("/api/flights")
def api_flights():
    return jsonify(FLIGHTS)

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/readyz")
def readyz():
    return "ready", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
