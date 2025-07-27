# Import mock Google ADK for development/testing
try:
    from google.adk.agents import SequentialAgent
except ImportError:
    print("Google ADK not found, using mock implementation...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    import mock_google_adk
    from google.adk.agents import SequentialAgent

from .subagents.soil_analysis_agent.agent import soil_analysis_agent
from .subagents.climate_matcher_agent.agent import climate_matcher_agent
from .subagents.crop_recommender_agent.agent import crop_recommender_agent

crop_advisory_agent = SequentialAgent(
    name="crop_advisory_agent",
    sub_agents=[
        soil_analysis_agent,
        climate_matcher_agent,
        crop_recommender_agent
    ],
    description="Sequential agent for soil analysis, climate matching, and optimal crop recommendations.",
) 