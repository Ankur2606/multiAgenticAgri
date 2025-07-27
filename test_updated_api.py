#!/usr/bin/env python3
"""
Test script for the updated agricultural agent API
This script tests the new functionality where session_id is optional in /agent/query
"""

import requests
import json
import time

# API Configuration
BASE_URL = "http://localhost:8000"
TEST_USER_ID = "test_farmer_123"

def test_api():
    """Test the updated API functionality"""
    
    print("🌾 Testing Agricultural Multi-Agent API Updates")
    print("=" * 50)
    
    # Test 1: Create a session
    print("\n1. Creating a new session...")
    
    session_data = {
        "app_name": "Agricultural Support",
        "user_id": TEST_USER_ID,
        "initial_state": {
            "user_name": "Test Farmer",
            "weather": "sunny",
            "weather_disc": "Clear skies with mild temperature",
            "precipitation": "0mm",
            "humidity": "65%",
            "windspeed": "12km/h",
            "location": "Maharashtra, India",
            "farm_size": "5 acres",
            "crop_type": "rice",
            "soil_type": "clay loam"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/session/create", json=session_data)
        response.raise_for_status()
        session_result = response.json()
        session_id = session_result['session_id']
        print(f"✅ Session created: {session_id}")
    except requests.RequestException as e:
        print(f"❌ Failed to create session: {e}")
        return False
    
    # Test 2: Query agent WITHOUT session_id (should use most recent)
    print("\n2. Testing agent query WITHOUT session_id...")
    
    query_data = {
        "user_id": TEST_USER_ID,
        "query": "What crops are suitable for my current weather conditions?"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/agent/query", json=query_data)
        response.raise_for_status()
        query_result = response.json()
        print(f"✅ Agent responded (session auto-selected: {query_result['session_id']})")
        print(f"📝 Response: {query_result['agent_response'][:100]}...")
    except requests.RequestException as e:
        print(f"❌ Failed to query agent without session_id: {e}")
    
    # Test 3: Query agent WITH specific session_id
    print("\n3. Testing agent query WITH specific session_id...")
    
    query_data_with_session = {
        "user_id": TEST_USER_ID,
        "session_id": session_id,
        "query": "Can you tell me about my current weather conditions?"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/agent/query", json=query_data_with_session)
        response.raise_for_status()
        query_result = response.json()
        print(f"✅ Agent responded (specific session: {query_result['session_id']})")
        print(f"📝 Response: {query_result['agent_response'][:100]}...")
    except requests.RequestException as e:
        print(f"❌ Failed to query agent with session_id: {e}")
    
    # Test 4: List user sessions
    print("\n4. Testing session listing...")
    
    try:
        response = requests.get(f"{BASE_URL}/sessions/{TEST_USER_ID}")
        response.raise_for_status()
        sessions_result = response.json()
        print(f"✅ Found {sessions_result['total_sessions']} sessions for user")
        print(f"📋 Sessions: {[s['session_id'][:8] + '...' for s in sessions_result['sessions']]}")
    except requests.RequestException as e:
        print(f"❌ Failed to list sessions: {e}")
    
    # Test 5: Get session details
    print("\n5. Testing session retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/session/{TEST_USER_ID}/{session_id}")
        response.raise_for_status()
        session_details = response.json()
        print(f"✅ Retrieved session details")
        print(f"📊 Interaction history: {len(session_details['interaction_history'])} entries")
        print(f"🌱 Farm info: {session_details['state'].get('crop_type', 'N/A')} on {session_details['state'].get('farm_size', 'N/A')}")
    except requests.RequestException as e:
        print(f"❌ Failed to get session details: {e}")
    
    print("\n" + "=" * 50)
    print("✅ API testing completed!")
    print("\n📋 Summary of changes:")
    print("- ✅ session_id is now optional in /agent/query")
    print("- ✅ API automatically uses most recent session when not specified")
    print("- ✅ Switched to DatabaseSessionService for persistent storage")
    print("- ✅ Enhanced session listing functionality")
    print("- ✅ Better error handling and feedback")

if __name__ == "__main__":
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        print("🚀 API server is running!")
        test_api()
    except requests.RequestException as e:
        print(f"❌ API server is not running. Please start it first with: python api_server.py")
        print(f"Error: {e}")
