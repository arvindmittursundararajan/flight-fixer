import os
import google.generativeai as genai
from google.adk.agents import LlmAgent
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY', 'YOUR_GOOGLE_API_KEY_HERE')

def echo_tool(text: str) -> str:
    print(f"Tool called: echo_tool with input: {text}")
    return text

async def get_agent():
    instruction = "You are a helpful assistant."
    agent = LlmAgent(
        name="test_agent",
        description="Minimal agent for automated testing",
        instruction=instruction,
        model="gemini-2.5-flash",
        tools=[echo_tool],
    )
    return agent 