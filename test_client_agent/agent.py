from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

campaign_agent = RemoteA2aAgent(
    name="campaign_agent",
    description="Agent that generates email campaigns by resolving projects, layouts, and audiences.",
    agent_card=
    (f"http://localhost:8001/a2a/campaign_agent{AGENT_CARD_WELL_KNOWN_PATH}"
     ),
)

root_agent = Agent(
    model='gemini-3-flash-preview',
    name='test_client_agent',
    description=
    "An agent that can generate email campaigns using the campaign_agent.",
    instruction=
    ("You are a helpful assistant that can generate email campaigns. "
     "To generate a campaign, use the 'campaign_agent' A2A agent. "
     "Pass the full user request to the campaign_agent."),
    sub_agents=[campaign_agent],
)
