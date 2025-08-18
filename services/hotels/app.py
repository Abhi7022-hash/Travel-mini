from flask import Flask, jsonify
app = Flask(__name__)

HOTELS = [
    {"id": 1, "name": "Sea View Inn", "city": "LAX", "price": 120},
    {"id": 2, "name": "Downtown Suites", "city": "NYC", "price": 200},
    {"id": 3, "name": "Airport Lodge", "city": "SFO", "price": 95}
]

@app.route("/api/hotels")
def api_hotels():
    return jsonify(HOTELS)

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/readyz")
def readyz():
    return "ready", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
