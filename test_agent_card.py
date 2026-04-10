import json
import os

def test_agent_card():
    print("Testing agent.json...")
    
    # Check if file exists
    assert os.path.exists("agent.json"), "agent.json file not found!"
    
    # Read and parse JSON
    with open("agent.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "agent.json is not a valid JSON file!"
            
    # Validate required fields
    required_fields = ["name", "description", "url", "skills"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
        
    print("agent.json is valid!")
    print(f"Agent Name: {data['name']}")
    print(f"URL: {data['url']}")
    print(f"Skills: {[s['name'] for s in data['skills']]}")

if __name__ == "__main__":
    try:
        test_agent_card()
    except AssertionError as e:
        print(f"Test Failed: {e}")
    else:
        print("All checks passed!")
