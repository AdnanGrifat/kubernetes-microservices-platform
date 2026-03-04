from flask import Flask, jsonify
import os, requests

app = Flask(__name__)
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:5000")

@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200

@app.get("/readyz")
def readyz():
    return jsonify(status="ready"), 200

@app.get("/order/<order_id>")
def get_order(order_id: str):
    # Example: call user-service
    user = requests.get(f"{USER_SERVICE_URL}/user/42", timeout=3).json()
    return jsonify(order_id=order_id, item="HVAC Filter", quantity=2, user=user), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
