from mcp.server.fastmcp import FastMCP

# Create an MCP server named "Sample Tools"
mcp = FastMCP("Sample Tools")

@mcp.tool()
def get_project_details(project_name: str) -> str:
    """Get details for a project from the database.
    
    This tool is intended to be called by the A2A agent to resolve
    fine-grained project details.
    """
    return f"Project '{project_name}' resolved to ID: proj_123 (Status: Active)."

@mcp.tool()
def get_layout_details(layout_name: str) -> str:
    """Get layout specifications."""
    return f"Layout '{layout_name}' resolved to ID: layout_abc (Type: Newsletter)."

@mcp.tool()
def get_audience_details(segment_name: str) -> str:
    """Get audience segment size and targeting criteria."""
    return f"Audience '{segment_name}' resolved to ID: seg_marketers (Size: 5000)."

if __name__ == "__main__":
    # This allows running the server directly for stdio transport
    mcp.run()
