# API Updates - Session Management Improvements

## Overview
This document describes the recent updates made to the Agricultural Multi-Agent API to improve session management and user experience.

## Key Changes

### 1. Optional Session ID in Agent Queries
**Endpoint:** `POST /agent/query`

**Before:**
```json
{
    "user_id": "farmer123",
    "session_id": "required-session-id",  // ❌ Required
    "query": "What crops should I plant?"
}
```

**After:**
```json
{
    "user_id": "farmer123",
    "session_id": "optional-session-id",  // ✅ Optional
    "query": "What crops should I plant?"
}
```

**Benefits:**
- **Simplified Usage**: Client applications no longer need to track session IDs
- **Automatic Session Selection**: API automatically uses the most recent session for the user
- **Better UX**: Reduces friction for end users
- **Backward Compatible**: Still accepts explicit session_id when provided

### 2. Enhanced Session Service
**Before:** `InMemorySessionService` (non-persistent, limited functionality)
**After:** `DatabaseSessionService` (persistent SQLite storage)

**Benefits:**
- **Persistent Storage**: Sessions survive server restarts
- **Session Listing**: Can retrieve all sessions for a user
- **Better Performance**: Optimized for production use
- **Scalability**: Ready for production deployment

### 3. Improved Session Management Endpoints

#### List User Sessions - `GET /sessions/{user_id}`
**Before:**
```json
{
    "message": "Session listing not implemented with InMemorySessionService",
    "note": "Consider using a persistent session service for this functionality"
}
```

**After:**
```json
{
    "user_id": "farmer123",
    "app_name": "Agricultural Support",
    "sessions": [
        {
            "session_id": "abc123...",
            "created_at": "2025-01-27T10:30:00",
            "last_modified": "2025-01-27T11:45:00"
        }
    ],
    "total_sessions": 1,
    "message": "Found 1 sessions for user farmer123"
}
```

#### Session Deletion - `DELETE /session/{user_id}/{session_id}`
- Enhanced validation
- Better error handling
- Clearer response messages

## API Behavior Changes

### Agent Query Logic
1. **With session_id provided**: Uses the specified session (same as before)
2. **Without session_id**: 
   - Automatically retrieves the most recent session for the user
   - Returns error if no sessions exist, prompting user to create one first
   - Updates the response to include the session_id that was used

### Error Handling
- **404 Error**: When no sessions exist for a user (without session_id)
- **Clear Messages**: Better error descriptions for troubleshooting
- **Graceful Degradation**: API continues to work even with agent processing errors

## Database File
The API now creates a SQLite database file: `agricultural_agent_sessions.db`
- **Location**: Same directory as `api_server.py`
- **Content**: All session data, user states, and interaction history
- **Backup**: Consider backing up this file for data persistence

## Migration Guide

### For Client Applications
1. **Optional Change**: Remove `session_id` from `/agent/query` requests to use automatic session selection
2. **Recommended**: Keep explicit `session_id` for applications that need precise session control
3. **New Feature**: Use `GET /sessions/{user_id}` to list all user sessions

### For Server Deployment
1. **Database**: The SQLite file will be created automatically
2. **Dependencies**: No additional dependencies required
3. **Backward Compatibility**: All existing API calls continue to work

## Testing
Use the provided test script to validate the changes:
```bash
# Start the API server
python api_server.py

# In another terminal, run tests
python test_updated_api.py
```

## Example Usage

### Simple Query (No Session Management)
```python
import requests

# User just needs to provide user_id and query
response = requests.post("http://localhost:8000/agent/query", json={
    "user_id": "farmer123",
    "query": "What's the best time to plant rice?"
})

result = response.json()
print(f"Agent response: {result['agent_response']}")
print(f"Used session: {result['session_id']}")
```

### Advanced Session Management
```python
import requests

# List all sessions for a user
sessions = requests.get("http://localhost:8000/sessions/farmer123").json()
print(f"User has {sessions['total_sessions']} sessions")

# Use a specific session
response = requests.post("http://localhost:8000/agent/query", json={
    "user_id": "farmer123",
    "session_id": sessions['sessions'][0]['session_id'],
    "query": "Continue our previous conversation about irrigation"
})
```

## Benefits Summary
- ✅ **Reduced Complexity**: Clients don't need to manage session IDs
- ✅ **Better Performance**: Persistent database storage
- ✅ **Enhanced Features**: Session listing and management
- ✅ **Backward Compatible**: Existing code continues to work
- ✅ **Production Ready**: SQLite database for reliable storage
- ✅ **Better UX**: Automatic session selection for seamless experience
