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