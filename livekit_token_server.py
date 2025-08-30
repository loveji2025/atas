import os
import time
import jwt
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET")


def create_livekit_token(api_key, api_secret, identity, room, ttl=3600):
    now = int(time.time())
    payload = {
        "iss": api_key,
        "sub": "",
        "nbf": now,
        "exp": now + ttl,
        "jti": f"{identity}-{now}",
        "grants": {
            "identity": identity,
            "video": {
                "roomJoin": True,
                "room": room
            }
        }
    }
    return jwt.encode(payload, api_secret, algorithm="HS256")

@app.route("/token", methods=["POST"])
def get_token():
    data = request.get_json(force=True)
    identity = data.get("identity")
    room = data.get("room", "default")
    token = create_livekit_token(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, identity, room)
    return jsonify({"token": token})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
