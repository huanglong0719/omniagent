import asyncio
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from app.memory.manager import OmniMemoryManager
from app.core.models import OmniMessage, Session

async def test_memory_performance():
    """Test memory operations performance."""
    print("=== Testing Memory Performance ===")
    memory_manager = OmniMemoryManager()
    session = Session(session_id="test_performance_session", user_id="test_user")
    
    # Test message insertion time
    start_time = time.time()
    for i in range(100):
        test_message = OmniMessage(
            message_id=f"test_msg_{i}",
            session_id="test_performance_session",
            sender="user",
            content=f"Test message {i} with some content to test memory operations",
            channel="console"
        )
        await memory_manager.add_message(test_message, session)
    insertion_time = time.time() - start_time
    print(f"✓ 100 messages inserted in: {insertion_time:.2f} seconds")
    
    # Test context retrieval time
    start_time = time.time()
    context = await memory_manager.get_context("test_performance_session")
    retrieval_time = time.time() - start_time
    print(f"✓ Context retrieved in: {retrieval_time:.2f} seconds")
    print(f"  Context size: {len(context)} messages")
    
    # Test semantic search time
    start_time = time.time()
    search_results = await memory_manager.semantic_search("test", "test_performance_session", limit=10)
    search_time = time.time() - start_time
    print(f"✓ Semantic search completed in: {search_time:.2f} seconds")
    print(f"  Search results: {len(search_results)}")
    
    return insertion_time, retrieval_time, search_time

async def test_concurrent_operations():
    """Test concurrent operations."""
    print("\n=== Testing Concurrent Operations ===")
    memory_manager = OmniMemoryManager()
    session = Session(session_id="test_concurrent_session", user_id="test_user")
    
    async def perform_operation(operation_id):
        """Perform a single operation."""
        # Insert a message
        test_message = OmniMessage(
            message_id=f"concurrent_msg_{operation_id}",
            session_id="test_concurrent_session",
            sender="user",
            content=f"Concurrent test message {operation_id}",
            channel="console"
        )
        await memory_manager.add_message(test_message, session)
        
        # Retrieve context
        context = await memory_manager.get_context("test_concurrent_session")
        
        # Perform semantic search
        search_results = await memory_manager.semantic_search("test", "test_concurrent_session", limit=5)
        
        return len(context), len(search_results)
    
    # Run 50 concurrent operations
    start_time = time.time()
    tasks = [perform_operation(i) for i in range(50)]
    results = await asyncio.gather(*tasks)
    concurrent_time = time.time() - start_time
    
    total_context_size = sum(result[0] for result in results)
    total_search_results = sum(result[1] for result in results)
    
    print(f"✓ 50 concurrent operations completed in: {concurrent_time:.2f} seconds")
    print(f"  Average context size: {total_context_size / 50:.1f} messages")
    print(f"  Average search results: {total_search_results / 50:.1f}")
    
    return concurrent_time

async def test_stress_test():
    """Test system under stress."""
    print("\n=== Testing Stress Test ===")
    memory_manager = OmniMemoryManager()
    session = Session(session_id="test_stress_session", user_id="test_user")
    
    # Test with 1000 messages
    start_time = time.time()
    for i in range(1000):
        test_message = OmniMessage(
            message_id=f"stress_msg_{i}",
            session_id="test_stress_session",
            sender="user",
            content=f"Stress test message {i} with some content to test system performance",
            channel="console"
        )
        await memory_manager.add_message(test_message, session)
    stress_time = time.time() - start_time
    print(f"✓ 1000 messages inserted in: {stress_time:.2f} seconds")
    print(f"  Average insertion time per message: {stress_time / 1000:.4f} seconds")
    
    # Test context retrieval after stress
    start_time = time.time()
    context = await memory_manager.get_context("test_stress_session")
    retrieval_time = time.time() - start_time
    print(f"✓ Context retrieved in: {retrieval_time:.2f} seconds")
    print(f"  Context size: {len(context)} messages")
    
    return stress_time, retrieval_time

async def run_performance_tests():
    """Run all performance tests."""
    print("Starting Performance Tests...")
    
    # Run memory performance test
    insertion_time, retrieval_time, search_time = await test_memory_performance()
    
    # Run concurrent operations test
    concurrent_time = await test_concurrent_operations()
    
    # Run stress test
    stress_time, stress_retrieval_time = await test_stress_test()
    
    # Print summary
    print("\n=== Performance Test Summary ===")
    print(f"Memory Operations:")
    print(f"  100 message insertion: {insertion_time:.2f}s")
    print(f"  Context retrieval: {retrieval_time:.2f}s")
    print(f"  Semantic search: {search_time:.2f}s")
    print(f"\nConcurrent Operations:")
    print(f"  50 concurrent operations: {concurrent_time:.2f}s")
    print(f"  Operations per second: {50 / concurrent_time:.2f} ops/s")
    print(f"\nStress Test:")
    print(f"  1000 message insertion: {stress_time:.2f}s")
    print(f"  Context retrieval after stress: {stress_retrieval_time:.2f}s")
    
    # Check if performance meets requirements
    print("\n=== Performance Evaluation ===")
    
    # Define performance thresholds
    thresholds = {
        "insertion_time": 5.0,  # seconds for 100 messages
        "retrieval_time": 2.0,  # seconds for context retrieval
        "search_time": 1.0,     # seconds for semantic search
        "concurrent_time": 10.0, # seconds for 50 concurrent operations
        "stress_time": 30.0     # seconds for 1000 messages
    }
    
    # Evaluate performance
    performance_metrics = {
        "insertion_time": insertion_time <= thresholds["insertion_time"],
        "retrieval_time": retrieval_time <= thresholds["retrieval_time"],
        "search_time": search_time <= thresholds["search_time"],
        "concurrent_time": concurrent_time <= thresholds["concurrent_time"],
        "stress_time": stress_time <= thresholds["stress_time"]
    }
    
    # Print evaluation results
    for metric, passed in performance_metrics.items():
        status = "✓" if passed else "✗"
        print(f"{status} {metric.replace('_', ' ')}: {locals()[metric]:.2f}s (threshold: {thresholds[metric]}s)")
    
    # Overall evaluation
    if all(performance_metrics.values()):
        print("\n✓ All performance metrics meet requirements!")
    else:
        print("\n✗ Some performance metrics do not meet requirements.")
    
    return all(performance_metrics.values())

if __name__ == "__main__":
    asyncio.run(run_performance_tests())
