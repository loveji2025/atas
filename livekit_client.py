import asyncio
import requests
from livekit import rtc

# ==== Tumhara LiveKit project URL ====
LIVEKIT_URL = "wss://atas-voice-assistant-k72sqixb.livekit.cloud"

# ==== Tumhara Render token server endpoint ====
TOKEN_SERVER_URL = "https://atas-nk8c.onrender.com/get_token"

async def connect_to_livekit():
    room = rtc.Room()

    # 1. Token Render server se fetch karo
    try:
        response = requests.get(TOKEN_SERVER_URL)
        response.raise_for_status()
        token = response.json().get("token")
        print(f"🔑 Got token: {token[:25]}... (truncated)")
    except Exception as e:
        print(f"❌ Failed to fetch token: {e}")
        return

    # 2. Callback jab connect ho jaye
    async def on_connected():
        print("✅ Connected to LiveKit room!")

    room.on("connected", on_connected)

    # 3. LiveKit connect karo
    try:
        print("🔗 Connecting to LiveKit...")
        await room.connect(LIVEKIT_URL, token)
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # 4. Room active rakho jab tak manually stop na ho
    await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    asyncio.run(connect_to_livekit())