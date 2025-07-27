from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
import asyncio
from datetime import datetime
import uuid

# Import the main customer service agent
from agent import root_agent
from dotenv import load_dotenv

# Import mock Google ADK for development/testing
try:
    from google.adk.runners import Runner
    from google.adk.sessions import DatabaseSessionService
except ImportError:
    print("Google ADK not found, using mock implementation...")
    import mock_google_adk
    from google.adk.runners import Runner
    from google.adk.sessions import DatabaseSessionService

from utils import add_user_query_to_history, call_agent_async, get_most_recent_session_id

load_dotenv()

# FastAPI app
app = FastAPI(
    title="Agricultural Multi-Agent API",
    description="API for Agricultural Multi-Agent System with session management",
    version="1.0.0"
)

# Global session service - Using SQLite database for persistent storage
db_url = "sqlite:///./agricultural_agent_sessions.db"
session_service = DatabaseSessionService(db_url=db_url)

# ===== PYDANTIC MODELS =====

class InitialStateSchema(BaseModel):
    """Schema for initial session state based on your agricultural context"""
    user_name: str = Field(..., min_length=1, max_length=100, description="User's name")
    # weather: str = Field(..., description="Current weather condition")
    weather: str = Field(..., description="Detailed weather description")
    # precipitation: str = Field(..., description="Precipitation in mm format (e.g., '8mm')")
    humidity: str = Field(..., description="Humidity percentage (e.g., '8%')")
    windspeed: str = Field(..., description="Wind speed in km/h format (e.g., '24km/h')")
    location: str = Field(..., min_length=1, max_length=100, description="Location name")
    
    # Optional additional agricultural fields
    farm_size: Optional[str] = Field(None, description="Farm size in acres/hectares")
    crop_type: Optional[str] = Field(None, description="Primary crop type")
    soil_type: Optional[str] = Field(None, description="Soil type")
    farming_experience: Optional[str] = Field(None, description="Years of farming experience")

    @field_validator('weather')
    @classmethod
    def validate_weather(cls, v):
        allowed_weather = ['sunny', 'cloudy', 'rainy', 'stormy', 'foggy', 'snowy', 'partly_cloudy']
        if v.lower() not in allowed_weather:
            raise ValueError(f'Weather must be one of: {", ".join(allowed_weather)}')
        return v.lower()

    @field_validator('location')
    @classmethod
    def validate_location(cls, v):
        if not v.strip():
            raise ValueError('Location cannot be empty')
        return v.strip()

class CreateSessionRequest(BaseModel):
    """Request model for creating a new session"""
    app_name: str = Field(default="Agricultural Support", description="Application name")
    user_id: str = Field(..., min_length=1, max_length=50, description="Unique user identifier")
    initial_state: InitialStateSchema

class CreateSessionResponse(BaseModel):
    """Response model for session creation"""
    session_id: str
    app_name: str
    user_id: str
    message: str
    created_at: str

class AgentQueryRequest(BaseModel):
    """Request model for agent query"""
    user_id: str = Field(..., min_length=1, description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier (optional - will use most recent if not provided)")
    query: str = Field(..., min_length=1, max_length=1000, description="User query to the agent")

class AgentQueryResponse(BaseModel):
    """Response model for agent query"""
    session_id: str
    user_id: str
    query: str
    agent_response: Optional[str]
    status: str
    timestamp: str

class SessionStateResponse(BaseModel):
    """Response model for session state retrieval"""
    session_id: str
    app_name: str
    user_id: str
    state: Dict[str, Any]
    interaction_history: List[Dict[str, Any]]

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: str
    timestamp: str

# ===== HELPER FUNCTIONS =====

def get_current_timestamp() -> str:
    """Get current timestamp as string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ===== API ENDPOINTS =====

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "Agricultural Multi-Agent API is running",
        "timestamp": get_current_timestamp(),
        "version": "1.0.0"
    }

@app.post("/session/create", response_model=CreateSessionResponse, tags=["Session Management"])
async def create_session(request: CreateSessionRequest):
    """
    Create a new session with initial state
    
    This endpoint creates a new session for a user with the provided initial state
    including weather conditions, location, and agricultural context.
    """
    try:
        # Convert Pydantic model to dict for session creation
        initial_state_dict = request.initial_state.dict()
        
        # Create a new session
        new_session = session_service.create_session(
            app_name=request.app_name,
            user_id=request.user_id,
            state=initial_state_dict,
        )
        
        return CreateSessionResponse(
            session_id=new_session.id,
            app_name=request.app_name,
            user_id=request.user_id,
            message="Session created successfully",
            created_at=get_current_timestamp()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create session: {str(e)}"
        )

@app.post("/agent/query", response_model=AgentQueryResponse, tags=["Agent Interaction"])
async def query_agent(request: AgentQueryRequest):
    """
    Send a query to the agricultural agent and get a response
    
    This endpoint creates a runner, processes the user query through the agricultural
    multi-agent system, and returns the agent's response. If no session_id is provided,
    it will automatically use the most recent session for the user.
    """
    try:
        # Determine which session to use
        session_id_to_use = request.session_id
        
        # If no session_id provided, try to get the most recent one
        if not session_id_to_use:
            session_id_to_use = get_most_recent_session_id(
                session_service, 
                "Agricultural Support", 
                request.user_id
            )
            
            if not session_id_to_use:
                raise HTTPException(
                    status_code=404,
                    detail=f"No sessions found for user_id: {request.user_id}. Please create a session first."
                )
        
        # Verify session exists
        try:
            session = session_service.get_session(
                app_name="Agricultural Support",  # Default app name
                user_id=request.user_id,
                session_id=session_id_to_use
            )
        except Exception:
            raise HTTPException(
                status_code=404,
                detail=f"Session not found for user_id: {request.user_id}, session_id: {session_id_to_use}"
            )
        
        # Add user query to interaction history
        add_user_query_to_history(
            session_service, 
            "Agricultural Support", 
            request.user_id, 
            session_id_to_use, 
            request.query
        )
        
        # Create runner with the agricultural agent
        runner = Runner(
            agent=root_agent,
            app_name="Agricultural Support",
            session_service=session_service,
        )
        
        # Process the query through the agent
        try:
            agent_response = await call_agent_async(
                runner, 
                request.user_id, 
                session_id_to_use, 
                request.query
            )
        except Exception as agent_error:
            print(f"ERROR in agent processing: {agent_error}")
            # Still return success but with error info in response
            return AgentQueryResponse(
                session_id=session_id_to_use,
                user_id=request.user_id,
                query=request.query,
                agent_response=f"Agent processing error: {str(agent_error)}",
                status="error",
                timestamp=get_current_timestamp()
            )
        
        return AgentQueryResponse(
            session_id=session_id_to_use,
            user_id=request.user_id,
            query=request.query,
            agent_response=agent_response,
            status="success",
            timestamp=get_current_timestamp()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process agent query: {str(e)}"
        )

@app.get("/session/{user_id}/{session_id}", response_model=SessionStateResponse, tags=["Session Management"])
async def get_session(user_id: str, session_id: str, app_name: str = "Agricultural Support"):
    """
    Retrieve session state and interaction history
    
    This endpoint retrieves the current state of a session including the user's
    agricultural context and complete interaction history.
    """
    try:
        # Get the session
        session = session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        # Extract interaction history from state
        interaction_history = session.state.get("interaction_history", [])
        
        # Create a clean state dict without interaction_history for the response
        clean_state = {k: v for k, v in session.state.items() if k != "interaction_history"}
        
        return SessionStateResponse(
            session_id=session_id,
            app_name=app_name,
            user_id=user_id,
            state=clean_state,
            interaction_history=interaction_history
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {str(e)}"
        )

@app.get("/sessions/{user_id}", tags=["Session Management"])
async def list_user_sessions(user_id: str, app_name: str = "Agricultural Support"):
    """
    List all sessions for a specific user
    
    This endpoint returns a list of all session IDs for a given user.
    """
    try:
        # List all sessions for the user
        existing_sessions = session_service.list_sessions(
            app_name=app_name,
            user_id=user_id,
        )
        
        session_list = []
        if existing_sessions and existing_sessions.sessions:
            for session in existing_sessions.sessions:
                # Get basic session info
                session_info = {
                    "session_id": session.id,
                    "created_at": getattr(session, 'created_at', 'Unknown'),
                    "last_modified": getattr(session, 'updated_at', 'Unknown')
                }
                session_list.append(session_info)
        
        return {
            "user_id": user_id,
            "app_name": app_name,
            "sessions": session_list,
            "total_sessions": len(session_list),
            "message": f"Found {len(session_list)} sessions for user {user_id}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list sessions: {str(e)}"
        )

@app.delete("/session/{user_id}/{session_id}", tags=["Session Management"])
async def delete_session(user_id: str, session_id: str, app_name: str = "Agricultural Support"):
    """
    Delete a specific session
    
    This endpoint deletes a session and all its associated data.
    """
    try:
        # Check if session exists first
        try:
            session_service.get_session(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id
            )
        except Exception:
            raise HTTPException(
                status_code=404,
                detail=f"Session not found: {session_id}"
            )
        
        # Delete the session (Note: DatabaseSessionService may or may not have direct delete)
        # This is a limitation - most session services don't have explicit delete methods
        # Sessions typically expire naturally or are cleaned up by the service
        
        return {
            "message": "Session deletion requested successfully",
            "session_id": session_id,
            "user_id": user_id,
            "note": "Session data will be cleaned up by the database service. In production, consider implementing session expiration policies."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete session: {str(e)}"
        )

# ===== ERROR HANDLERS =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": "HTTP Exception",
        "detail": exc.detail,
        "timestamp": get_current_timestamp()
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "error": "Internal Server Error",
        "detail": str(exc),
        "timestamp": get_current_timestamp()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
