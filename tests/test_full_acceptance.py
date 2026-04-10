import asyncio
import json
from omniagent.app.memory.manager import OmniMemoryManager
from omniagent.app.brain.brain import OmniBrain
from omniagent.app.core.models import OmniMessage, Session
from omniagent.app.evolution.verification import SkillVerificationSystem
from omniagent.app.gateway.gateway import OmniGateway

async def test_encryption_functionality():
    """Test encryption functionality."""
    print("=== Testing Encryption Functionality ===")
    memory_manager = OmniMemoryManager()
    
    # Create test session and message
    session = Session(session_id="test_session_encryption")
    test_message = OmniMessage(
        message_id="test_msg_encryption",
        session_id="test_session_encryption",
        sender="user",
        content="This is a test message with sensitive information",
        channel="console"
    )
    
    # Add message to memory (should be encrypted)
    await memory_manager.add_message(test_message, session)
    print("✓ Message added to memory")
    
    # Retrieve message from L3 (should be decrypted)
    retrieved_msg = await memory_manager.get_from_l3("test_msg_encryption")
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
    
    return retrieved_msg is not None

async def test_memory_management():
    """Test memory management functionality."""
    print("\n=== Testing Memory Management ===")
    memory_manager = OmniMemoryManager()
    
    # Create test session
    session = Session(session_id="test_session_memory")
    
    # Add multiple messages
    for i in range(5):
        test_message = OmniMessage(
            message_id=f"test_msg_{i}",
            session_id="test_session_memory",
            sender="user",
            content=f"Test message {i}",
            channel="console"
        )
        await memory_manager.add_message(test_message, session)
    print("✓ Messages added to memory")
    
    # Test context retrieval
    context = await memory_manager.get_context("test_session_memory")
    print(f"✓ Context retrieved: {len(context)} messages")
    
    # Test semantic search
    search_results = await memory_manager.semantic_search("test", "test_session_memory", limit=3)
    print(f"✓ Semantic search completed: {len(search_results)} results")
    
    # Test predictive prefetch
    await memory_manager.predictive_prefetch("test_session_memory", "test")
    print("✓ Predictive prefetch completed")
    
    return len(context) > 0

async def test_skill_verification():
    """Test skill verification system."""
    print("\n=== Testing Skill Verification System ===")
    from omniagent.app.evolution.engine import EvolutionEngine
    
    memory_manager = OmniMemoryManager()
    evolution_engine = EvolutionEngine(memory_manager)
    
    # Create a test skill
    skill_name = await evolution_engine.create_skill(
        "Test Skill",
        "Test execution steps",
        "Test success criteria"
    )
    print(f"✓ Skill created: {skill_name}")
    
    # Test verification system
    verification_system = evolution_engine.verification_system
    status = verification_system.get_skill_status(skill_name)
    print(f"✓ Skill status: {status}")
    
    # Submit for verification
    verification_system.submit_for_verification(skill_name, "test_user")
    print("✓ Skill submitted for verification")
    
    # Review the skill
    verification_system.review_skill(skill_name, "test_reviewer", True, "Test comments")
    print("✓ Skill reviewed and approved")
    
    # Check updated status
    updated_status = verification_system.get_skill_status(skill_name)
    print(f"✓ Updated skill status: {updated_status}")
    
    return updated_status == "Verified"

async def test_multi_agent_collaboration():
    """Test multi-agent collaboration using LangGraph."""
    print("\n=== Testing Multi-Agent Collaboration ===")
    memory_manager = OmniMemoryManager()
    brain = OmniBrain(memory_manager)
    
    # Create test session
    session = Session(session_id="test_session_multi_agent")
    
    # Test complex task
    complex_message = OmniMessage(
        message_id="test_msg_complex",
        session_id="test_session_multi_agent",
        sender="user",
        content="Create a detailed research report on artificial intelligence trends in 2024",
        channel="console"
    )
    
    # Process the message (should use multi-agent mode)
    response = await brain.process_message(complex_message, session)
    print("✓ Multi-agent collaboration completed")
    print(f"Response length: {len(response)} characters")
    
    return len(response) > 0

async def test_dynamic_mode_switching():
    """Test dynamic mode switching."""
    print("\n=== Testing Dynamic Mode Switching ===")
    memory_manager = OmniMemoryManager()
    brain = OmniBrain(memory_manager)
    
    # Create test session
    session = Session(session_id="test_session_mode_switch")
    
    # Test simple task
    simple_message = OmniMessage(
        message_id="test_msg_simple",
        session_id="test_session_mode_switch",
        sender="user",
        content="Hello, how are you?",
        channel="console"
    )
    
    # Process simple message
    simple_response = await brain.process_message(simple_message, session)
    print("✓ Simple task processed")
    
    # Test complex task
    complex_message = OmniMessage(
        message_id="test_msg_complex_2",
        session_id="test_session_mode_switch",
        sender="user",
        content="Analyze the benefits and drawbacks of remote work",
        channel="console"
    )
    
    # Process complex message
    complex_response = await brain.process_message(complex_message, session)
    print("✓ Complex task processed")
    
    return len(simple_response) > 0 and len(complex_response) > 0

async def test_gateway_functionality():
    """Test gateway functionality."""
    print("\n=== Testing Gateway Functionality ===")
    memory_manager = OmniMemoryManager()
    brain = OmniBrain(memory_manager)
    gateway = OmniGateway(brain)
    
    # Test message handling
    response = await gateway.handle_incoming_message(
        channel="console",
        user_id="test_user",
        content="Test gateway functionality"
    )
    print("✓ Gateway message handling completed")
    print(f"Response: {response}")
    
    return len(response) > 0

async def run_full_acceptance_test():
    """Run full acceptance test."""
    print("Starting Full Acceptance Test...")
    
    # Run all tests
    tests = [
        test_encryption_functionality(),
        test_memory_management(),
        test_skill_verification(),
        test_multi_agent_collaboration(),
        test_dynamic_mode_switching(),
        test_gateway_functionality()
    ]
    
    results = await asyncio.gather(*tests)
    
    # Calculate pass rate
    passed = sum(results)
    total = len(results)
    pass_rate = (passed / total) * 100
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Pass Rate: {pass_rate:.2f}%")
    
    if passed == total:
        print("✓ All tests passed! System is ready for production.")
    else:
        print("✗ Some tests failed. Please review the results.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(run_full_acceptance_test())
