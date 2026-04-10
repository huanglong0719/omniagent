from typing import Dict, Any, Optional, List
from app.core.models import OmniMessage, Session
from app.security.privacy_filter import PrivacyFilter
from app.gateway.adapters import ChannelAdapter, TelegramAdapter, WhatsAppAdapter
import uuid
import asyncio

class OmniGateway:
    """
    OmniGateway: The Control Plane for OmniAgent.
    Handles multi-channel routing, session management, and privacy filtering.
    """
    
    def __init__(self, brain):
        self.brain = brain
        self.privacy_filter = PrivacyFilter()
        self.sessions: Dict[str, Session] = {}
        self.adapters: Dict[str, ChannelAdapter] = {}

    def register_adapter(self, adapter: ChannelAdapter):
        """Register a channel adapter."""
        self.adapters[adapter.get_channel_name()] = adapter
        print(f"[Gateway] Registered adapter: {adapter.get_channel_name()}")

    async def start_adapters(self):
        """Start all registered adapters."""
        for adapter in self.adapters.values():
            if hasattr(adapter, 'start_polling'):
                await adapter.start_polling()

    async def stop_adapters(self):
        """Stop all registered adapters."""
        for adapter in self.adapters.values():
            if hasattr(adapter, 'stop_polling'):
                await adapter.stop_polling()

    async def handle_incoming_message(self, channel: str, user_id: str, content: str) -> str:
        """
        Main entry point for all incoming messages.
        """
        # 1. Session Management
        session_id = self._get_or_create_session(user_id)
        session = self.sessions[session_id]
        
        # 2. Privacy Filtering (Task 0)
        filtered_content, entities = self.privacy_filter.filter_text(content)
        
        # 3. Create Unified Message
        message = OmniMessage(
            session_id=session_id,
            sender="user",
            content=filtered_content,
            channel=channel
        )
        
        # 4. Route to OmniBrain
        print(f"[Gateway] Routing message from {channel} (User: {user_id}) to OmniBrain")
        response_content = await self.brain.process_message(message, session)
        
        # 5. Post-process response (Privacy Filter again for AI output)
        final_response, _ = self.privacy_filter.filter_text(response_content)
        
        return final_response

    async def send_message(self, channel: str, recipient: str, content: str) -> bool:
        """Send a message through the specified channel."""
        if channel in self.adapters:
            return await self.adapters[channel].send_message(recipient, content)
        else:
            print(f"[Gateway] Adapter not found for channel: {channel}")
            return False

    async def poll_messages(self):
        """Poll all adapters for incoming messages."""
        while True:
            for channel, adapter in self.adapters.items():
                message_data = await adapter.receive_message()
                if message_data:
                    print(f"[Gateway] Received message from {channel}: {message_data}")
                    # Process the message
                    response = await self.handle_incoming_message(
                        channel=message_data['channel'],
                        user_id=message_data['user_id'],
                        content=message_data['content']
                    )
                    # Send response back through the same channel
                    recipient = message_data.get('chat_id', message_data['user_id'])
                    await self.send_message(channel, recipient, response)
            await asyncio.sleep(0.1)

    def _get_or_create_session(self, user_id: str) -> str:
        # In a real system, we'd look up the user_id in the DB to find their session_id
        # For demo, we use a simple mapping or create a new one
        for sid, session in self.sessions.items():
            if session.user_id == user_id:
                return sid
        
        new_session = Session(user_id=user_id)
        self.sessions[new_session.session_id] = new_session
        return new_session.session_id
