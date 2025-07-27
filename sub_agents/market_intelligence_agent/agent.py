from google.adk.agents import ParallelAgent
from .subagents.price_collector_agent.agent import price_collector_agent
from .subagents.blockchain_validator_agent.agent import blockchain_validator_agent
from .subagents.anomaly_detector_agent.agent import anomaly_detector_agent
from .subagents.recommendation_engine_agent.agent import recommendation_engine_agent

market_intelligence_agent = ParallelAgent(
    name="market_intelligence_agent",
    sub_agents=[
        price_collector_agent,
        blockchain_validator_agent,
        anomaly_detector_agent,
        recommendation_engine_agent
    ],
    description="Parallel agent with blockchain integration for real-time mandi prices, community validation, anomaly detection, and selling recommendations.",
) 