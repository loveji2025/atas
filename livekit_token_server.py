from fastapi import FastAPI
from fastapi.responses import JSONResponse
from livekit.api import AccessToken, VideoGrants
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Token server running"}

# 🔑 Environment variables (Render me set karna hoga)
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://atas-voice-assistant-k72sqixb.livekit.cloud")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "your_api_key_here")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "your_api_secret_here")

@app.get("/get_token")
def get_token(identity: str = "testuser", room: str = "testroom"):
    try:
        # Check if API credentials are properly set
        if not LIVEKIT_API_KEY or LIVEKIT_API_KEY == "your_api_key_here":
            return JSONResponse({"error": "LIVEKIT_API_KEY not set or using placeholder"}, status_code=500)
        if not LIVEKIT_API_SECRET or LIVEKIT_API_SECRET == "your_api_secret_here":
            return JSONResponse({"error": "LIVEKIT_API_SECRET not set or using placeholder"}, status_code=500)

        # AccessToken generate
        token = AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        token.identity = identity
        token.addGrant(VideoGrants(room_join=True, room=room))
        jwt = token.to_jwt()

        return JSONResponse({"token": jwt})
    except Exception as e:
        print(f"Error generating token: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)