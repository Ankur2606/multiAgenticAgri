"""
Mock Google ADK classes and functions for testing and development purposes.
This allows the multi-agent system to work without the actual Google ADK installed.
"""

class Agent:
    """Mock Agent class"""
    def __init__(self, name=None, model=None, description=None, instruction=None, tools=None, sub_agents=None):
        self.name = name
        self.model = model
        self.description = description
        self.instruction = instruction
        self.tools = tools or []
        self.sub_agents = sub_agents or []
        
    def __str__(self):
        return f"MockAgent(name={self.name})"
        
    async def run(self, message, context=None):
        """Mock run method that returns a simple response"""
        return f"Mock response from {self.name}: Processed '{message}'"

class SequentialAgent(Agent):
    """Mock SequentialAgent class"""
    def __init__(self, name=None, sub_agents=None, description=None):
        super().__init__(name=name, description=description, sub_agents=sub_agents)
        
    async def run(self, message, context=None):
        """Mock sequential processing"""
        responses = []
        for i, agent in enumerate(self.sub_agents):
            response = await agent.run(message, context)
            responses.append(f"Step {i+1}: {response}")
        return " -> ".join(responses)

class AgentTool:
    """Mock AgentTool class"""
    def __init__(self, agent=None):
        self.agent = agent
        
    def __call__(self, *args, **kwargs):
        """Mock tool execution"""
        if self.agent:
            return f"Tool result from {self.agent.name}: {args} {kwargs}"
        return f"Tool result: {args} {kwargs}"

class Runner:
    """Mock Runner class"""
    def __init__(self, agent=None, app_name=None, session_service=None):
        self.agent = agent
        self.app_name = app_name
        self.session_service = session_service
        
    async def run(self, user_id, session_id, message):
        """Mock runner execution"""
        if self.agent:
            return await self.agent.run(message)
        return f"Mock runner response to: {message}"

class DatabaseSessionService:
    """Mock DatabaseSessionService class"""
    def __init__(self, db_url=None):
        self.db_url = db_url
        self.sessions = {}
        
    def create_session(self, app_name, user_id, state=None):
        """Mock session creation"""
        import uuid
        session_id = str(uuid.uuid4())
        session = MockSession(session_id, app_name, user_id, state or {})
        self.sessions[session_id] = session
        return session
        
    def get_session(self, app_name, user_id, session_id):
        """Mock session retrieval"""
        if session_id in self.sessions:
            return self.sessions[session_id]
        raise Exception(f"Session {session_id} not found")
        
    def update_session(self, app_name, user_id, session_id, state):
        """Mock session update"""
        if session_id in self.sessions:
            self.sessions[session_id].state.update(state)
            return self.sessions[session_id]
        raise Exception(f"Session {session_id} not found")
        
    def list_sessions(self, app_name, user_id):
        """Mock session listing"""
        user_sessions = [s for s in self.sessions.values() 
                        if s.user_id == user_id and s.app_name == app_name]
        return MockSessionList(user_sessions)

class MockSession:
    """Mock Session class"""
    def __init__(self, session_id, app_name, user_id, state):
        self.id = session_id
        self.app_name = app_name
        self.user_id = user_id
        self.state = state
        import datetime
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

class MockSessionList:
    """Mock SessionList class"""
    def __init__(self, sessions):
        self.sessions = sessions

# Mock google_search function
def google_search(query):
    """Mock Google search function"""
    return f"Mock Google search results for: {query}. This would normally return web search results about crop diseases, treatments, and agricultural information."

# Create mock modules structure
class MockTools:
    google_search = google_search

class MockAgents:
    Agent = Agent
    SequentialAgent = SequentialAgent

class MockToolsModule:
    agent_tool = type('AgentTool', (), {'AgentTool': AgentTool})

class MockRunners:
    Runner = Runner

class MockSessions:
    DatabaseSessionService = DatabaseSessionService

class MockGoogleADK:
    agents = MockAgents()
    tools = MockTools()
    runners = MockRunners()
    sessions = MockSessions()

# Create the mock google module structure
import sys
import types

# Create mock google module
google_module = types.ModuleType('google')
adk_module = types.ModuleType('google.adk')
agents_module = types.ModuleType('google.adk.agents')
tools_module = types.ModuleType('google.adk.tools')
agent_tool_module = types.ModuleType('google.adk.tools.agent_tool')
runners_module = types.ModuleType('google.adk.runners')
sessions_module = types.ModuleType('google.adk.sessions')

# Add classes to modules
agents_module.Agent = Agent
agents_module.SequentialAgent = SequentialAgent
tools_module.google_search = google_search
agent_tool_module.AgentTool = AgentTool
runners_module.Runner = Runner
sessions_module.DatabaseSessionService = DatabaseSessionService

# Build module hierarchy
google_module.adk = adk_module
adk_module.agents = agents_module
adk_module.tools = tools_module
adk_module.runners = runners_module
adk_module.sessions = sessions_module
tools_module.agent_tool = agent_tool_module

# Register modules
sys.modules['google'] = google_module
sys.modules['google.adk'] = adk_module
sys.modules['google.adk.agents'] = agents_module
sys.modules['google.adk.tools'] = tools_module
sys.modules['google.adk.tools.agent_tool'] = agent_tool_module
sys.modules['google.adk.runners'] = runners_module
sys.modules['google.adk.sessions'] = sessions_module

print("Mock Google ADK modules created successfully!")
