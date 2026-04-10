# mcp_server.py
# This file simulates the customer's existing MCP server exposing tools.
# It uses the FastMCP pattern (standard for building MCP servers in Python).

from mcp.server.fastmcp import FastMCP

# Create an MCP server named "Typeface Tools"
mcp = FastMCP("Typeface Tools")

# --- Architectural Note ---
# Depending on how you deploy this, the transport mechanism will change:
# 1. Co-located (Recommended): If this runs in the same container as the A2A agent,
#    it will communicate via 'stdio' (standard input/output).
# 2. Distributed: If this runs as a separate service, you would expose it via 'SSE'
#    (Server-Sent Events) over HTTP.
# ---------------------------

@mcp.tool()
def get_project_details(project_name: str) -> str:
    """Retrieves details for a specific project.
    
    Args:
        project_name: The name of the project to look up.
    """
    # Mock implementation
    return f"Project '{project_name}' details: ID=proj_123, Status=Active, Description=April Product Launch."

@mcp.tool()
def get_layout_details(layout_name: str) -> str:
    """Retrieves details for a specific email layout.
    
    Args:
        layout_name: The name of the layout to look up.
    """
    # Mock implementation
    return f"Layout '{layout_name}' details: ID=layout_abc, Type=Newsletter, Sections=[Header, Hero, Body, CTA]."

@mcp.tool()
def get_audience_details(segment_name: str) -> str:
    """Retrieves details for an audience segment.
    
    Args:
        segment_name: The name of the segment to look up.
    """
    # Mock implementation
    return f"Audience '{segment_name}' details: ID=seg_marketers, Size=5000, Criteria=[job_title=marketer]."

if __name__ == "__main__":
    # By default, FastMCP runs over stdio.
    # For SSE, you would use mcp.run(transport="sse") or similar depending on the library version.
    mcp.run()
