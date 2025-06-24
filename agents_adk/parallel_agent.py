import os
import google.generativeai as genai
from google.adk.agents import LlmAgent, ParallelAgent
from dotenv import load_dotenv

# Set up Google API key from environment variable
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY', 'YOUR_GOOGLE_API_KEY_HERE')

load_dotenv()

def echo_tool(text: str) -> str:
    return text

def add_tool(a: float, b: float) -> float:
    return a + b

async def get_agent():
    echo_agent = LlmAgent(
        name="echo_agent_parallel",
        description="Echoes user input (parallel).",
        instruction="Echo the user's message.",
        model="gemini-2.5-flash",
        tools=[echo_tool],
    )
    math_agent = LlmAgent(
        name="math_agent_parallel",
        description="Adds two numbers (parallel).",
        instruction="Add two numbers provided by the user.",
        model="gemini-2.5-flash",
        tools=[add_tool],
    )
    par_agent = ParallelAgent(
        name="parallel_agent",
        sub_agents=[echo_agent, math_agent],
        description="Runs echo_agent and math_agent in parallel."
    )
    return par_agent 