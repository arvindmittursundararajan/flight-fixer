import os
import google.generativeai as genai
from google.adk.agents import LlmAgent, SequentialAgent
from dotenv import load_dotenv
from google_adk import Agent, AgentConfig, AgentContext, AgentResponse

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY', 'YOUR_GOOGLE_API_KEY_HERE')

def echo_tool(text: str) -> str:
    return text

def add_tool(a: float, b: float) -> float:
    return a + b

async def get_agent():
    echo_agent = LlmAgent(
        name="echo_agent",
        description="Echoes user input.",
        instruction="Echo the user's message.",
        model="gemini-2.5-flash",
        tools=[echo_tool],
    )
    math_agent = LlmAgent(
        name="math_agent",
        description="Adds two numbers.",
        instruction="Add two numbers provided by the user.",
        model="gemini-2.5-flash",
        tools=[add_tool],
    )
    seq_agent = SequentialAgent(
        name="sequential_agent",
        sub_agents=[echo_agent, math_agent],
        description="Runs echo_agent then math_agent in sequence."
    )
    return seq_agent 