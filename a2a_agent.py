# a2a_agent.py
# This file demonstrates the A2A head agent that fronts the MCP server.
# It handles the orchestration Sandeep was concerned about.

from google.adk.agents.llm_agent import Agent
from typing import Dict, Any

# --- Architectural Note ---
# RECOMMENDED PATTERN: Co-locate this A2A Agent and the MCP Server in the same
# Cloud Run container. The A2A Agent can spawn the MCP server as a subprocess
# and communicate via 'stdio'. This keeps the orchestration and tools in one
# secure, low-latency box controlled by you (the ISV).
# ---------------------------

# Helper to simulate calling the MCP server.
# In a production environment with co-location, this would use an MCP client
# library to communicate with 'mcp_server.py' over stdio pipes.
def call_mcp(tool_name: str, arguments: Dict[str, Any]) -> str:
    print(f"[A2A Agent -> MCP] Invoking tool '{tool_name}' with arguments: {arguments}")
    
    # Simulated responses from the MCP server
    if tool_name == "get_project_details":
        return f"Project '{arguments.get('project_name')}' resolved to ID: proj_123 (Status: Active)."
    elif tool_name == "get_layout_details":
        return f"Layout '{arguments.get('layout_name')}' resolved to ID: layout_abc (Type: Newsletter)."
    elif tool_name == "get_audience_details":
        return f"Audience '{arguments.get('segment_name')}' resolved to ID: seg_marketers (Size: 5000)."
    else:
        return "Error: Tool not found."

# We expose these helper functions as ADK tools.
# The LLM in the A2A agent will decide when and how to call them.
def get_project(project_name: str) -> str:
    """Resolves project details by calling the MCP server."""
    return call_mcp("get_project_details", {"project_name": project_name})

def get_layout(layout_name: str) -> str:
    """Resolves layout details by calling the MCP server."""
    return call_mcp("get_layout_details", {"layout_name": layout_name})

def get_audience(segment_name: str) -> str:
    """Resolves audience details by calling the MCP server."""
    return call_mcp("get_audience_details", {"segment_name": segment_name})

# Define the A2A Agent
root_agent = Agent(
    model='gemini-3-flash-preview',
    name='typeface_a2a_head',
    description="Typeface A2A Head Agent that orchestrates MCP tools to generate campaigns.",
    instruction=(
        "You are the Typeface A2A Head Agent. "
        "When a user asks to generate an email campaign, you MUST orchestrate the following steps: "
        "1. Call 'get_project' to resolve the project details. "
        "2. Call 'get_layout' to resolve the layout details. "
        "3. Call 'get_audience' to resolve the audience details. "
        "4. Finally, use all the gathered information to generate a comprehensive email campaign summary. "
        "This demonstrates that YOU (the A2A agent) are handling the orchestration, not the calling platform (Gemini Enterprise)."
    ),
    tools=[get_project, get_layout, get_audience],
)
