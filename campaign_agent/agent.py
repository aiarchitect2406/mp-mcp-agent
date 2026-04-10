from google.adk.agents.llm_agent import Agent
from typing import Dict, Any

def get_project_details(project_name: str) -> Dict[str, Any]:
    """Retrieves details for a specific project.
    
    Args:
        project_name: The name of the project to look up.
    """
    print(f"[Tool] Resolving project: {project_name}")
    return {
        "project_name": project_name,
        "id": "proj_123",
        "description": "Launch of a new product in April",
        "status": "active"
    }

def get_layout_details(layout_name: str) -> Dict[str, Any]:
    """Retrieves details for a specific email layout.
    
    Args:
        layout_name: The name of the layout to look up.
    """
    print(f"[Tool] Resolving layout: {layout_name}")
    return {
        "layout_name": layout_name,
        "id": "layout_abc",
        "type": "newsletter",
        "sections": ["header", "hero_image", "body_text", "cta"]
    }

def get_audience_details(segment_name: str) -> Dict[str, Any]:
    """Retrieves details for an audience segment.
    
    Args:
        segment_name: The name of the segment to look up.
    """
    print(f"[Tool] Resolving audience: {segment_name}")
    return {
        "segment_name": segment_name,
        "id": "seg_marketers",
        "size": 5000,
        "targeting_criteria": ["job_title=marketer", "industry=tech"]
    }

root_agent = Agent(
    model='gemini-3-flash-preview',
    name='campaign_agent',
    description="An agent that generates email campaigns by resolving projects, layouts, and audiences.",
    instruction=(
        "You are a helpful assistant that generates email campaigns. "
        "To generate a campaign, you MUST first find the details of the specified project, "
        "layout, and audience segment using the provided tools. "
        "Once you have all the details, generate a summary of the campaign including the project ID, layout ID, and audience size."
    ),
    tools=[get_project_details, get_layout_details, get_audience_details],
)
