import asyncio
import sys
import os

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from a2a_agent import root_agent, call_mcp

async def run_scenario(name, prompt, simulate_logic):
    print(f"\n=== Scenario: {name} ===")
    print(f"[Gemini Enterprise -> A2A Agent] Prompt: {prompt}\n")
    await simulate_logic()
    print("=" * 40)

async def test_e2e_simulation():
    print("Starting E2E Orchestration Simulation with Robustness Scenarios...")
    
    # Scenario 1: Happy Path
    async def scenario_1():
        print("[A2A Agent] Starting orchestration...")
        proj = call_mcp("get_project_details", {"project_name": "April Launch"})
        layout = call_mcp("get_layout_details", {"layout_name": "Launch Layout"})
        aud = call_mcp("get_audience_details", {"segment_name": "Marketers"})
        
        campaign = (
            f"Campaign Summary:\n"
            f"- Project: {proj}\n"
            f"- Layout: {layout}\n"
            f"- Audience: {aud}\n"
            f"Campaign generated successfully!"
        )
        print(f"\n[A2A Agent -> Gemini Enterprise] Response:\n{campaign}")

    await run_scenario("Full Information (Happy Path)", 
                       "Generate an email campaign for April Launch, using Launch Layout for Marketers.", 
                       scenario_1)

    # Scenario 2: Missing Information (Handling incomplete requests)
    async def scenario_2():
        print("[A2A Agent] Starting orchestration...")
        proj = call_mcp("get_project_details", {"project_name": "April Launch"})
        aud = call_mcp("get_audience_details", {"segment_name": "Marketers"})
        
        print("\n[A2A Agent] Notice: Layout was not specified in the request.")
        print("[A2A Agent] Strategy: Falling back to default layout or asking user.")
        
        campaign = (
            f"Campaign Summary (Draft):\n"
            f"- Project: {proj}\n"
            f"- Layout: PENDING (Please specify a layout)\n"
            f"- Audience: {aud}\n"
            f"I have gathered the project and audience details, but I need you to specify a layout to complete the campaign."
        )
        print(f"\n[A2A Agent -> Gemini Enterprise] Response:\n{campaign}")

    await run_scenario("Missing Layout (Graceful Degradation)", 
                       "Generate a campaign for April Launch targeted at Marketers.", 
                       scenario_2)

    # Scenario 3: Invalid Input (Error Handling)
    async def scenario_3():
        print("[A2A Agent] Starting orchestration...")
        
        # Simulate tool call returning error
        print("[A2A Agent -> MCP] Invoking tool 'get_project_details' with arguments: {'project_name': 'Unknown Project'}")
        result = "Error: Project not found."
        print(f"[A2A Agent] Result: {result}")
        
        print("\n[A2A Agent] Strategy: Aborting generation and informing user of the specific error.")
        
        response = "I'm sorry, I couldn't find a project named 'Unknown Project'. Please verify the project name and try again."
        print(f"\n[A2A Agent -> Gemini Enterprise] Response:\n{response}")

    await run_scenario("Invalid Project (Error Handling)", 
                       "Generate a campaign for Unknown Project using Launch Layout.", 
                       scenario_3)

if __name__ == "__main__":
    asyncio.run(test_e2e_simulation())
