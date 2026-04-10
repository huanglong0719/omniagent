import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.security.privacy_filter import PrivacyFilter
from app.core.models import OmniMessage, Session
from app.memory.manager import OmniMemoryManager
from app.brain.brain import OmniBrain
from app.gateway.gateway import OmniGateway
from app.gateway.adapters import TelegramAdapter, WhatsAppAdapter
from app.api.endpoints import app as api_app

app = FastAPI(title="OmniAgent API")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含 API 路由
app.mount("/api", api_app)

# Initialize Components
memory_manager = OmniMemoryManager()
brain = OmniBrain(memory_manager=memory_manager)
gateway = OmniGateway(brain=brain)

# Register channel adapters (you'll need to set your own tokens)
# For demo purposes, we'll use placeholder tokens
telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"
whatsapp_account_sid = "YOUR_TWILIO_ACCOUNT_SID"
whatsapp_auth_token = "YOUR_TWILIO_AUTH_TOKEN"
whatsapp_phone_number = "YOUR_TWILIO_PHONE_NUMBER"

if telegram_token != "YOUR_TELEGRAM_BOT_TOKEN":
    telegram_adapter = TelegramAdapter(token=telegram_token)
    gateway.register_adapter(telegram_adapter)

if whatsapp_account_sid != "YOUR_TWILIO_ACCOUNT_SID":
    whatsapp_adapter = WhatsAppAdapter(
        account_sid=whatsapp_account_sid,
        auth_token=whatsapp_auth_token,
        phone_number=whatsapp_phone_number
    )
    gateway.register_adapter(whatsapp_adapter)

# Start adapters and message polling
async def start_services():
    await gateway.start_adapters()
    # Start message polling in a background task
    asyncio.create_task(gateway.poll_messages())

# Start services when the app starts
@app.on_event("startup")
async def startup_event():
    await start_services()

# Stop services when the app stops
@app.on_event("shutdown")
async def shutdown_event():
    await gateway.stop_adapters()

class ChatRequest(BaseModel):
    session_id: str
    user_id: str
    content: str
    channel: str

@app.get("/")
async def root():
    return {"status": "OmniAgent is running", "version": "0.1.0"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Use the Gateway to handle the request (integrates PrivacyFilter, Session, and Brain)
        response = await gateway.handle_incoming_message(
            channel=request.channel,
            user_id=request.user_id,
            content=request.content
        )
        return {
            "response": response,
            "session_id": request.session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
