from google.adk import Agent
from google.adk.tools.mcp_tool import McpToolset
from mcp import StdioServerParameters

# Define the connection to the local MCP server
# We use python to run mcp_server.py
toolset = McpToolset(
    connection_params=StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )
)

# Define the A2A Head Agent
root_agent = Agent(
    name='sample_a2a_head',
    description="Sample A2A Head Agent that orchestrates MCP tools to generate campaigns.",
    instruction=(
        "You are the Sample A2A Head Agent. "
        "Your job is to fulfill user requests by orchestrating calls to underlying MCP tools. "
        "When a user asks to generate a campaign, you MUST ALWAYS call the tools first to resolve details, "
        "even if you think you have the information in the prompt. "
        "Do not ask the user for clarification until you have tried calling the tools.\n"
        "1. Call 'get_project_details' to resolve the project.\n"
        "2. Call 'get_layout_details' to resolve the layout.\n"
        "3. Call 'get_audience_details' to resolve the audience.\n"
        "4. Combine this information to produce the final campaign output."
    ),
    tools=[toolset]
)

