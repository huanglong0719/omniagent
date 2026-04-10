from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class ChannelAdapter(ABC):
    """Base class for all channel adapters."""
    
    @abstractmethod
    async def send_message(self, recipient: str, content: str) -> bool:
        """Send a message to the recipient.
        
        Args:
            recipient: The recipient identifier (e.g., chat ID for Telegram)
            content: The message content
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    async def receive_message(self) -> Optional[Dict[str, Any]]:
        """Receive a message from the channel.
        
        Returns:
            Optional[Dict[str, Any]]: Message data if a message was received, None otherwise
        """
        pass
    
    @abstractmethod
    def get_channel_name(self) -> str:
        """Get the name of the channel.
        
        Returns:
            str: Channel name
        """
        pass
