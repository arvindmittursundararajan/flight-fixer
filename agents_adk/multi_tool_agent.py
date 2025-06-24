from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google_adk import Agent, AgentConfig, AgentContext, AgentResponse
from google_adk.agents import AgentRegistry
from google_adk.tools import Tool, ToolRegistry
from google_adk.workflows import Workflow, WorkflowRegistry
from google_adk.workflows.workflow_engine import WorkflowEngine
from google_adk.workflows.workflow_executor import WorkflowExecutor
from google_adk.workflows.workflow_scheduler import WorkflowScheduler

# Load environment variables and set API key directly for robustness
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY', 'YOUR_GOOGLE_API_KEY_HERE')

APP_NAME = "basic_agent_no_web"
USER_ID = "user_12345"
SESSION_ID = "session_12345"

# Step 0: Define a simple tool
def echo_tool(text: str) -> str:
    """Echoes the input text."""
    return text

# Step 1: get the agent
async def get_agent():
    # Try to load instruction from prompt.txt
    prompt_file = "prompt.txt"
    if os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as f:
            instruction = f.read().strip()
    else:
        instruction = "You are a helpful assistant."
    root_agent = LlmAgent(
        name="first_agent",
        description="This is my first agent",
        instruction=instruction,
        model="gemini-2.5-flash",
        tools=[echo_tool],
    )
    return root_agent

# Step 2: run the agent
async def main(query):
    # create memory session
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    # get the agent
    root_agent = await get_agent()

    # create runner instance
    runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)

    # format the query
    content = types.Content(role="user", parts=[types.Part(text=query)])

    print("Running agent with query:", query)
    # run the agent
    events = runner.run_async(
        new_message=content,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    # print the response
    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response:", final_response)

if __name__ == "__main__":
    asyncio.run(main("Echo this: FORMAT21 works!")) 