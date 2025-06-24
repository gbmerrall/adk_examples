import os
import sys
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.tools import VertexAiSearchTool, google_search
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools.agent_tool import AgentTool

# Load environment variables from .env file at module level
load_dotenv(override=True)


def setup_vertex_ai_environment():

    # Remove any API key that might interfere
    if "GOOGLE_API_KEY" in os.environ:
        del os.environ["GOOGLE_API_KEY"]

    # Print environment state after changes
    print("\nEnvironment after setup:")
    print(f"GOOGLE_GENAI_USE_VERTEXAI: {os.environ.get('GOOGLE_GENAI_USE_VERTEXAI')}")
    print(f"GOOGLE_API_KEY exists: {'GOOGLE_API_KEY' in os.environ}")
    print(f"GOOGLE_CLOUD_PROJECT: {os.environ.get('GOOGLE_CLOUD_PROJECT')}")
    print(f"GOOGLE_CLOUD_LOCATION: {os.environ.get('GOOGLE_CLOUD_LOCATION')}")
    print(f"Running in ADK web context: {'adk' in sys.argv[0] if sys.argv else False}\n")

# Set up environment at module level
setup_vertex_ai_environment()

# Replace with your actual Vertex AI Search Datastore ID
YOUR_DATASTORE_ID = "projects/dasfreak/locations/global/collections/default_collection/dataStores/nz-crimes_1750223742957"

# Tool Instantiation
vertex_search_tool = VertexAiSearchTool(data_store_id=YOUR_DATASTORE_ID)

# Create the search agent with its own tools
search_agent = LlmAgent(
    name="basic_search_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions using Google Search.",
    instruction="I can answer your questions by searching the internet. Just ask me anything!",
    tools=[google_search],
)

doc_qa_agent = LlmAgent(
    name="doc_qa_agent",
    model="gemini-2.0-flash", # Requires Gemini model
    tools=[vertex_search_tool],
    instruction=f"""You are a helpful assistant that answers questions based on information found in the document store: {YOUR_DATASTORE_ID}.
    Use the search tool to find relevant information before answering.
    If the answer isn't in the documents, say that you couldn't find the information.
    """,
    description="Answers questions using a specific Vertex AI Search datastore.",
)

code_agent = LlmAgent(
    name="calculator_agent",
    model="gemini-2.0-flash",
    code_executor=BuiltInCodeExecutor(),
    instruction="""You are a calculator agent.
    When given a mathematical expression, write and execute Python code to calculate the result.
    Return only the final numerical result as plain text, without markdown or code blocks.
    """,
    description="Executes Python code to perform calculations.",
)

# Wrap the specialized agents as tools
search_tool = AgentTool(agent=search_agent)
doc_qa_tool = AgentTool(agent=doc_qa_agent)
code_tool = AgentTool(agent=code_agent)

# Create the root agent with the search agent
root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash",
    tools=[search_tool, doc_qa_tool, code_tool],
    instruction="""You are a helpful assistant that can answer questions and perform calculations.
    You have 2 specialized agents to choose from:
    - basic_search_agent: to search the internet
    - doc_qa_agent: to answer questions based on the document store
    - calculator_agent: to perform calculations

    The user will provide a question which defines where the answer should come from, 
    and you should delegate to the appropriate agent to find the answer.
    """,
    description="A helpful assistant that can answer questions and perform calculations."
)