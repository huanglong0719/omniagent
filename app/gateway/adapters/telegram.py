from typing import Optional, Dict, Any
from omniagent.app.gateway.adapters.base import ChannelAdapter
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

class TelegramAdapter(ChannelAdapter):
    """Telegram channel adapter."""
    
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=token)
        self.application = None
        self.message_queue = asyncio.Queue()
    
    async def send_message(self, recipient: str, content: str) -> bool:
        """Send a message to a Telegram chat."""
        try:
            await self.bot.send_message(chat_id=recipient, text=content)
            return True
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
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
        return "telegram"
    
    async def start_polling(self):
        """Start polling for Telegram messages."""
        self.application = Application.builder().token(self.token).build()
        
        # Register handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._message_handler))
        
        # Start polling
        await self.application.start_polling()
        print("Telegram adapter started polling")
    
    async def stop_polling(self):
        """Stop polling for Telegram messages."""
        if self.application:
            await self.application.stop_polling()
            print("Telegram adapter stopped polling")
    
    async def _message_handler(self, update: Update, context):
        """Handle incoming Telegram messages."""
        message = update.message
        if message:
            message_data = {
                "channel": "telegram",
                "user_id": str(message.from_user.id),
                "content": message.text,
                "chat_id": str(message.chat.id)
            }
            await self.message_queue.put(message_data)
