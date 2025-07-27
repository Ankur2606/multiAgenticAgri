# Agricultural Multi-Agent API

A FastAPI-based REST API for the Agricultural Multi-Agent System that provides session management and agent interaction capabilities.

## Features

- **Session Management**: Create and manage user sessions with agricultural context
- **Agent Interaction**: Query the multi-agent system for agricultural advice
- **State Persistence**: Maintain user state and interaction history
- **Pydantic Validation**: Strong input validation with detailed error messages
- **Interactive Documentation**: Auto-generated API docs with Swagger UI

## API Endpoints

### 1. Create Session
**POST** `/session/create`

Creates a new session with initial agricultural state.

```json
{
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
```

### 2. Query Agent
**POST** `/agent/query`

Send queries to the agricultural multi-agent system.

```json
{
  "user_id": "farmer_001",
  "session_id": "your_session_id",
  "query": "What crops should I plant given the current weather conditions?"
}
```

### 3. Get Session State
**GET** `/session/{user_id}/{session_id}`

Retrieve current session state and interaction history.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_api.txt
```

### 2. Set Up Environment
Make sure you have your `.env` file with the necessary API keys for the Google ADK.

### 3. Start the Server
```bash
# Option 1: Direct Python
python api_server.py

# Option 2: Using the batch script (Windows)
start_api_server.bat

# Option 3: Using uvicorn directly
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the API
- **Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Testing

Run the test client to verify all endpoints:

```bash
python test_api_client.py
```

## Pydantic Schema Validation

The API includes comprehensive input validation:

### Initial State Schema
- **user_name**: Required string (1-100 chars)
- **weather**: Must be one of: sunny, cloudy, rainy, stormy, foggy, snowy, partly_cloudy
- **precipitation**: Must match pattern: `^\d+(\.\d+)?mm$` (e.g., "8mm")
- **humidity**: Must match pattern: `^\d+(\.\d+)?%$` (e.g., "8%")
- **windspeed**: Must match pattern: `^\d+(\.\d+)?km/h$` (e.g., "24km/h")
- **location**: Required string (1-100 chars)
- **farm_size**: Optional string
- **crop_type**: Optional string
- **soil_type**: Optional string

### Example Valid Requests

#### Create Session
```bash
curl -X POST "http://localhost:8000/session/create" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "Agricultural Support",
    "user_id": "farmer_001",
    "initial_state": {
      "user_name": "John Farmer",
      "weather": "sunny",
      "weather_disc": "Clear skies with high temperature",
      "precipitation": "0mm",
      "humidity": "45%",
      "windspeed": "15km/h",
      "location": "Punjab"
    }
  }'
```

#### Query Agent
```bash
curl -X POST "http://localhost:8000/agent/query" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "farmer_001",
    "session_id": "your_session_id",
    "query": "What fertilizer should I use for wheat in this weather?"
  }'
```

#### Get Session
```bash
curl -X GET "http://localhost:8000/session/farmer_001/your_session_id"
```

## Error Handling

The API provides detailed error responses:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Session not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side errors

## Architecture

```
api_server.py
├── FastAPI Application
├── Pydantic Models (Input Validation)
├── Session Management (InMemorySessionService)
├── Agent Runner (Google ADK)
└── Error Handling
```

## Dependencies

- **FastAPI**: Modern web framework for APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for FastAPI
- **Google ADK**: Agricultural agent development kit
- **Python-dotenv**: Environment variable management

## Development

To extend the API:

1. Add new Pydantic models in the models section
2. Create new endpoints following the existing pattern
3. Update the test client with new test cases
4. Update this README with new endpoint documentation

## Production Considerations

For production deployment:

1. Replace `InMemorySessionService` with a persistent storage solution
2. Add authentication and authorization
3. Implement rate limiting
4. Add logging and monitoring
5. Use environment-specific configuration
6. Add CORS middleware if needed for web frontend
7. Use a production ASGI server like Gunicorn with Uvicorn workers

## Support

For issues or questions about the API, please refer to the main project documentation or contact the development team.
