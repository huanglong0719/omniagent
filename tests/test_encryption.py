import asyncio
from omniagent.app.memory.manager import OmniMemoryManager
from omniagent.app.core.models import OmniMessage, MemoryTier, Session
from datetime import datetime

async def test_encryption():
    """Test encryption functionality."""
    print("Testing encryption functionality...")
    
    # Create memory manager
    memory_manager = OmniMemoryManager()
    
    # Create test session
    session = Session(session_id="test_session_1")
    
    # Create test message
    test_message = OmniMessage(
        message_id="test_msg_1",
        session_id="test_session_1",
        sender="user",
        content="This is a test message with sensitive information",
        timestamp=datetime.now(),
        channel="console",
        tier=MemoryTier.L3
    )
    
    # Add message to memory (should be encrypted)
    await memory_manager.add_message(test_message, session)
    print("✓ Message added to memory")
    
    # Retrieve message from L3 (should be decrypted)
    retrieved_msg = await memory_manager.get_from_l3("test_msg_1")
    if retrieved_msg:
        print(f"✓ Message retrieved from L3")
        print(f"Original content: {test_message.content}")
        print(f"Retrieved content: {retrieved_msg.content}")
        
        if retrieved_msg.content == test_message.content:
            print("✓ Encryption/decryption working correctly")
        else:
            print("✗ Encryption/decryption failed")
    else:
        print("✗ Failed to retrieve message")
    
    print("Encryption test completed!")

if __name__ == "__main__":
    asyncio.run(test_encryption())
