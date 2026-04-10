import asyncio
from omniagent.app.gateway.gateway import OmniGateway
from omniagent.app.brain.brain import OmniBrain
from omniagent.app.memory.manager import OmniMemoryManager
from omniagent.app.core.models import Session

async def run_test():
    # Setup
    memory = OmniMemoryManager()
    brain = OmniBrain(memory_manager=memory)
    gateway = OmniGateway(brain=brain)
    
    user_id = "user_123"
    
    print("--- Test 1: Basic Chat & Privacy Filter ---")
    res1 = await gateway.handle_incoming_message(
        channel="telegram", 
        user_id=user_id, 
        content="Hello! My email is test@example.com"
    )
    print(f"Response: {res1}")
    # Check if email is masked in the brain's memory (via internal check)
    # We can't easily check internal state here, but we can check the response
    
    print("\\n--- Test 2: Complex Task (Multi-Agent) ---")
    res2 = await gateway.handle_incoming_message(
        channel="whatsapp", 
        user_id=user_id, 
        content="Please research the AI agent market and write a report"
    )
    print(f"Response: {res2}")
    
    print("\\n--- Test 3: Skill Evolution ---")
    # Trigger evolution by saying thanks
    res3 = await gateway.handle_incoming_message(
        channel="web", 
        user_id=user_id, 
        content="Thanks, that was correct!"
    )
    print(f"Response: {res3}")
    
    print("\\n--- Test 4: Skill Retrieval ---")
    # Send a query that should match the evolved skill (General Task)
    res4 = await gateway.handle_incoming_message(
        channel="telegram", 
        user_id=user_id, 
        content="I have a general task for you"
    )
    print(f"Response: {res4}")

if __name__ == "__main__":
    asyncio.run(run_test())
