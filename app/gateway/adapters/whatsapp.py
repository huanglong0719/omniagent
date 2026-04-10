from typing import Optional, Dict, Any
from app.gateway.adapters.base import ChannelAdapter
from twilio.rest import Client
import asyncio

class WhatsAppAdapter(ChannelAdapter):
    """WhatsApp channel adapter using Twilio API."""
    
    def __init__(self, account_sid: str, auth_token: str, phone_number: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.phone_number = phone_number
        self.client = Client(account_sid, auth_token)
        self.message_queue = asyncio.Queue()
    
    async def send_message(self, recipient: str, content: str) -> bool:
        """Send a message to a WhatsApp user."""
        try:
            message = self.client.messages.create(
                from_=f'whatsapp:{self.phone_number}',
                body=content,
                to=f'whatsapp:{recipient}'
            )
            return True
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False
    
    async def receive_message(self) -> Optional[Dict[str, Any]]:
        """Receive a message from the message queue."""
        try:
            # Wait for a message with timeout
            message_data = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
            return message_data
        except asyncio.TimeoutError:
            return None
    
    def get_channel_name(self) -> str:
        """Get the channel name."""
        return "whatsapp"
    
    def process_incoming_webhook(self, data: Dict[str, Any]):
        """Process incoming webhook data from Twilio."""
        # This method would be called by a webhook endpoint
        # For now, we'll just simulate putting a message in the queue
        message_data = {
            "channel": "whatsapp",
            "user_id": data.get("From", "").replace("whatsapp:", ""),
            "content": data.get("Body", ""),
            "message_sid": data.get("MessageSid", "")
        }
        asyncio.create_task(self.message_queue.put(message_data))
