import os
import google.generativeai as genai
from google.adk.agents import LlmAgent, LoopAgent
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY', 'YOUR_GOOGLE_API_KEY_HERE')

def echo_tool(text: str) -> str:
    return text

async def get_agent():
    echo_agent = LlmAgent(
        name="echo_agent_loop",
        description="Echoes user input (loop).",
        instruction="Echo the user's message.",
        model="gemini-2.5-flash",
        tools=[echo_tool],
    )
    loop_agent = LoopAgent(
        name="loop_agent",
        sub_agents=[echo_agent],
        max_iterations=2,
        description="Runs echo_agent in a loop for 2 iterations."
    )
    return loop_agent 