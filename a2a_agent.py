from google.adk import Agent
import json
import subprocess

# Define the A2A Head Agent
root_agent = Agent(
    name='sample_a2a_head',
    description="Sample A2A Head Agent that orchestrates MCP tools to generate campaigns.",
    system_instruction=(
        "You are the Sample A2A Head Agent. "
        "Your job is to fulfill user requests by orchestrating calls to underlying MCP tools. "
        "When a user asks to generate a campaign, you must:\n"
        "1. Call 'get_project_details' to resolve the project.\n"
        "2. Call 'get_layout_details' to resolve the layout.\n"
        "3. Call 'get_audience_details' to resolve the audience.\n"
        "4. Combine this information to produce the final campaign output."
    )
)

# Simulated MCP Client call
# In a real production environment, this would use the MCP SDK to connect
# to the MCP server via stdio or SSE.
def call_mcp(tool_name: str, arguments: dict) -> str:
    """Simulates calling an MCP tool."""
    print(f"[A2A Agent -> MCP] Invoking tool '{tool_name}' with arguments: {arguments}")
    
    # For simulation, we just call the python script directly or mock the output
    # In a real co-located setup, you would use:
    # process = subprocess.Popen(['python', 'mcp_server.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    
    if tool_name == "get_project_details":
        return f"Project '{arguments.get('project_name')}' resolved to ID: proj_123 (Status: Active)."
    elif tool_name == "get_layout_details":
        return f"Layout '{arguments.get('layout_name')}' resolved to ID: layout_abc (Type: Newsletter)."
    elif tool_name == "get_audience_details":
        return f"Audience '{arguments.get('segment_name')}' resolved to ID: seg_marketers (Size: 5000)."
    else:
        return f"Error: Unknown tool {tool_name}"

# Expose tools to the ADK agent (these are the high-level tools the agent thinks it has)
@root_agent.tool
def get_project(project_name: str) -> str:
    """Get details for a project."""
    return call_mcp("get_project_details", {"project_name": project_name})

@root_agent.tool
def get_layout(layout_name: str) -> str:
    """Get details for a layout."""
    return call_mcp("get_layout_details", {"layout_name": layout_name})

@root_agent.tool
def get_audience(segment_name: str) -> str:
    """Get details for an audience segment."""
    return call_mcp("get_audience_details", {"segment_name": segment_name})
