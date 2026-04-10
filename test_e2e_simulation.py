import asyncio
import sys
import os
from google.adk import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sample_a2a_head.agent import root_agent

async def run_scenario(name, prompt):
    print(f"\n=== Scenario: {name} ===")
    print(f"[User] Prompt: {prompt}\n")
    
    # Create the runner
    runner = Runner(
        app_name="campaign_agent",
        agent=root_agent,
        session_service=InMemorySessionService(),
        auto_create_session=True
    )
    
    # Run the agent
    # We use run_async since we are in an async function
    events = runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=types.Content(parts=[types.Part.from_text(text=prompt)])
    )
    
    async for event in events:
        # Print the event to see what's happening
        if event.content:
             for part in event.content.parts:
                 if part.text:
                     print(f"[Agent Response]: {part.text}")
                 elif part.function_call:
                     print(f"[Tool Call]: {part.function_call.name}({part.function_call.args})")
                 elif part.function_response:
                     print(f"[Tool Response]: {part.function_response.response}")
    
    print("=" * 40)

async def test_e2e():
    print("Starting Real E2E Orchestration Test with MCP...")
    
    # Scenario 1: Happy Path
    await run_scenario("Full Information (Happy Path)", 
                       "Generate an email campaign for Product Launch, using Launch Layout for Marketers.")

    # Scenario 2: Missing Information
    await run_scenario("Missing Layout", 
                       "Generate a campaign for Product Launch targeted at Marketers.")

    # Scenario 3: Invalid Input
    await run_scenario("Invalid Project", 
                       "Generate a campaign for Unknown Project using Launch Layout.")

if __name__ == "__main__":
    asyncio.run(test_e2e())

