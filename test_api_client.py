"""
Test script for the Agricultural Multi-Agent API
Run this after starting the API server with: python api_server.py
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    """Test all three main API endpoints"""
    
    print("🌾 Testing Agricultural Multi-Agent API")
    print("=" * 50)
    
    # Test 1: Create Session
    print("\n1. Creating a new session...")
    
    session_data = {
        "app_name": "Agricultural Support",
        "user_id": "farmer_001",
        "initial_state": {
            "user_name": "Brandon Hancock",
            "weather": "sunny",
            "weather_disc": "weirdly hot",
            "precipitation": "8mm",
            "humidity": "8%",
            "windspeed": "24km/h",
            "location": "Gwalior",
            "farm_size": "5 acres",
            "crop_type": "wheat",
            "soil_type": "loamy"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/session/create", json=session_data)
        if response.status_code == 200:
            session_response = response.json()
            session_id = session_response["session_id"]
            print(f"✅ Session created successfully!")
            print(f"   Session ID: {session_id}")
            print(f"   User ID: {session_response['user_id']}")
        else:
            print(f"❌ Failed to create session: {response.status_code}")
            print(response.text)
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Make sure it's running on localhost:8000")
        return
    
    # Test 2: Query Agent
    print("\n2. Querying the agricultural agent...")
    
    query_data = {
        "user_id": "farmer_001",
        "session_id": session_id,
        "query": "Hello"
        
    }
    
    try:
        response = requests.post(f"{BASE_URL}/agent/query", json=query_data)
        if response.status_code == 200:
            query_response = response.json()
            print(f"✅ Agent query successful!")
            print(f"   Query: {query_response['query']}")
            print(f"   Status: {query_response['status']}")
            print(f"   Timestamp: {query_response['timestamp']}")
            
            agent_response = query_response.get('agent_response')
            if agent_response:
                # Show first 200 characters of response
                if len(agent_response) > 200:
                    print(f"   Agent Response: {agent_response[:200]}...")
                else:
                    print(f"   Agent Response: {agent_response}")
            else:
                print(f"   Agent Response: None (Check server logs for potential issues)")
                print(f"   Full Response: {json.dumps(query_response, indent=2)}")
        else:
            print(f"❌ Failed to query agent: {response.status_code}")
            print(f"   Error details: {response.text}")
    except Exception as e:
        print(f"❌ Error querying agent: {e}")
    
    # Test 3: Get Session State
    print("\n3. Retrieving session state...")
    
    try:
        response = requests.get(f"{BASE_URL}/session/farmer_001/{session_id}")
        if response.status_code == 200:
            session_state = response.json()
            print(f"✅ Session state retrieved successfully!")
            print(f"   User: {session_state['state'].get('user_name', 'Unknown')}")
            print(f"   Location: {session_state['state'].get('location', 'Unknown')}")
            print(f"   Weather: {session_state['state'].get('weather', 'Unknown')}")
            print(f"   Interactions: {len(session_state['interaction_history'])} recorded")
        else:
            print(f"❌ Failed to get session state: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error getting session state: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")

def test_validation():
    """Test Pydantic validation with invalid data"""
    
    print("\n🧪 Testing Pydantic validation...")
    
    # Test with invalid weather
    invalid_data = {
        "app_name": "Agricultural Support",
        "user_id": "farmer_002",
        "initial_state": {
            "user_name": "Test User",
            "weather": "invalid_weather",  # Invalid weather
            "weather_disc": "test",
            "precipitation": "invalid_format",  # Invalid format
            "humidity": "8%",
            "windspeed": "24km/h",
            "location": "Test Location"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/session/create", json=invalid_data)
        if response.status_code == 422:
            print("✅ Validation working correctly - rejected invalid data")
            errors = response.json()
            print(f"   Validation errors: {len(errors.get('detail', []))}")
            # Show first validation error as example
            if errors.get('detail'):
                first_error = errors['detail'][0]
                print(f"   Example error: {first_error.get('msg', 'Unknown error')}")
        else:
            print(f"❌ Validation not working properly: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing validation: {e}")

def test_agent_response_debugging():
    """Additional test to debug agent response issues"""
    
    print("\n🔍 Debugging agent response...")
    
    # Create a simple session first
    session_data = {
        "app_name": "Agricultural Support",
        "user_id": "debug_user",
        "initial_state": {
            "user_name": "Debug User",
            "weather": "sunny",
            "weather_disc": "clear",
            "precipitation": "0mm",
            "humidity": "50%",
            "windspeed": "10km/h",
            "location": "Test Farm"
        }
    }
    
    try:
        # Create session
        session_response = requests.post(f"{BASE_URL}/session/create", json=session_data)
        if session_response.status_code != 200:
            print(f"❌ Failed to create debug session: {session_response.status_code}")
            return
            
        session_id = session_response.json()["session_id"]
        print(f"✅ Debug session created: {session_id}")
        
        # Test different query complexities
        test_queries = [
            "Hello",
            "Hello, can you help me with farming?",
            "What is the weather like?",
            "What crops should I plant?",
            "What crops should I plant in sunny weather?",
            "What crops should I plant given the current weather conditions in Gwalior?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Test {i}: '{query}'")
            
            simple_query = {
                "user_id": "debug_user",
                "session_id": session_id,
                "query": query
            }
            
            query_response = requests.post(f"{BASE_URL}/agent/query", json=simple_query)
            
            if query_response.status_code == 200:
                response_data = query_response.json()
                agent_response = response_data.get('agent_response')
                
                if agent_response:
                    if len(agent_response) > 80:
                        print(f"   ✅ Response: {agent_response[:80]}...")
                    else:
                        print(f"   ✅ Response: {agent_response}")
                else:
                    print(f"   ❌ Response: None")
            else:
                print(f"   ❌ Query failed: {query_response.status_code}")
                
    except Exception as e:
        print(f"❌ Debug test error: {e}")

if __name__ == "__main__":
    # Test basic functionality
    test_api()
    
    # Test validation
    test_validation()
    
    # Debug agent response issues
    test_agent_response_debugging()
    
    print("\n📝 API Documentation available at: http://localhost:8000/docs")
    print("📊 Alternative docs at: http://localhost:8000/redoc")
    print("\n💡 Troubleshooting tips:")
    print("   - Check server logs for agent processing errors")
    print("   - Verify your .env file has the correct API keys")
    print("   - Ensure all agent dependencies are properly imported")
