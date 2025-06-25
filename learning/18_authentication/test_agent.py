#!/usr/bin/env python3
"""
Test script to verify the agent can connect to the FastAPI server.
"""

import asyncio
from agent import root_agent

async def test_agent():
    """Test the agent's ability to connect and make API calls."""
    if root_agent is None:
        print("❌ Agent is None - OpenAPI spec could not be fetched")
        return
    
    print("✅ Agent created successfully")
    print(f"Agent name: {root_agent.name}")
    print(f"Number of tools: {len(root_agent.tools)}")
    
    # Test a simple query
    try:
        print("\n🧪 Testing agent with query: 'List all pets'")
        response = await root_agent.run_async("List all pets")
        print("✅ Agent response received successfully")
        print(f"Response: {response}")
    except Exception as e:
        print(f"❌ Error testing agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent()) 