# Import mock Google ADK for development/testing
try:
    from google.adk.agents import Agent
except ImportError:
    print("Google ADK not found, using mock implementation...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    import mock_google_adk
    from google.adk.agents import Agent

from tools.crop_tools import firebase_disease_search

database_search_agent = Agent(
    name="database_search_agent",
    model="gemini-2.5-flash-lite",
    description="Agent for searching a vector-embedded Firebase database for crop disease diagnosis based on symptoms, crop, crop part, and location.",
    instruction="""
    You are the Database Search Agent for Crop Care. Your job is to search a vector-embedded Firebase database for crop disease diagnosis.

    **Your Capabilities:**
    1. Accept user input including crop, symptoms, affected crop part, and location.
    2. Query the Firebase database for the most similar entry using vector similarity search.
    3. If the similarity score is above a set threshold, return the matching disease object with all relevant details.
    4. If no match is found above the threshold, return None and suggest the user provide more details or a clearer image.

    **Session State Context:**
    Access weather information from the user's session state which includes current {weather}, {weather_disc}, {precipitation}, {humidity}, {windspeed} and {location}.
    Use this weather context to enhance disease diagnosis accuracy and provide weather-specific recommendations.

    Always provide clear, concise, and actionable results. If uncertain, ask for more information.
    """,
    tools=[firebase_disease_search],
)