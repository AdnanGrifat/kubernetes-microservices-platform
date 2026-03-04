from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200

@app.get("/readyz")
def readyz():
    return jsonify(status="ready"), 200

@app.get("/user/<user_id>")
def get_user(user_id: str):
    # Demo payload
    return jsonify(user_id=user_id, name=f"User-{user_id}", tier="standard"), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
