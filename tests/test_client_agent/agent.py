from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

head_agent = RemoteA2aAgent(
    name="sample_a2a_head",
    description="Sample A2A Head Agent that orchestrates MCP tools to generate campaigns.",
    agent_card=(
        f"http://localhost:8001/a2a/sample_a2a_head{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

root_agent = Agent(
    model='gemini-3-flash-preview',
    name='test_client_agent',
    description="An agent that can generate email campaigns using the sample_a2a_head.",
    instruction=(
        "You are a helpful assistant that can generate email campaigns. "
        "To generate a campaign, use the 'sample_a2a_head' A2A agent. "
        "Pass the full user request to the sample_a2a_head."
    ),
    sub_agents=[head_agent],
)
