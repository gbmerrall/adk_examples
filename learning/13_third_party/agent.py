import os
import re
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.tools.langchain_tool import LangchainTool
from langchain_tavily import TavilySearch
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper

# Load environment variables from .env file at module level
load_dotenv(override=True)

for env_var in [
    "GITHUB_APP_ID",
    "GITHUB_APP_PRIVATE_KEY",
    "GITHUB_REPOSITORY",
    "TAVILY_API_KEY",
]:
    if not os.getenv(env_var):
        print(f"Warning: {env_var} environment variable not set.")

# Instantiate the LangChain tool
tavily_tool_instance = TavilySearch(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=5,
    search_depth="advanced",
    include_images=True,
    include_raw_content=True,
    include_answer=True,
)
adk_tavily_tool = LangchainTool(tool=tavily_tool_instance)

# Instantiate the GitHub toolkit

tools_list = [
    "Get Issues",
    "Get Issue",
    "Comment on Issue",
    "List open pull requests (PRs)",
    "Get Pull Request",
    "Overview of files included in PR",
    "Create Pull Request",
    "List Pull Requests' Files",
    "Create File",
    "Read File",
    "Update File",
    "Delete File",
    "Overview of existing files in Main branch",
    "Overview of files in current working branch",
    "List branches in this repository",
    "Set active branch",
    "Create a new branch",
    "Get files from a directory",
    "Search issues and pull requests",
    "Search code",
    "Create review request",
]

github_repository = os.getenv("GITHUB_REPOSITORY")
if not github_repository:
    raise ValueError(
        "Please set the GITHUB_REPOSITORY environment variable to your repository "
        "(e.g., 'owner/repo')."
    )

github_api_wrapper = GitHubAPIWrapper(
    github_repository=github_repository,
    github_app_id=os.getenv("GITHUB_APP_ID"),
    github_app_private_key=os.getenv("GITHUB_APP_PRIVATE_KEY"),
)

toolkit = GitHubToolkit.from_github_api_wrapper(github_api_wrapper)

# Sanitize all tool names for Gemini compatibility
github_tools = []
for t in toolkit.get_tools():
    sanitized_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", t.name)
    github_tools.append(LangchainTool(tool=t, name=sanitized_name))

root_agent = LlmAgent(
    name="langchain_tool_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions using TavilySearch and GitHub.",
    instruction=f"""I can answer your questions by searching the internet or interacting with GitHub. Just ask me anything!
    For github tools, the list of available tools is:{tools_list}
    For everything else, use the tavily search tool.
    """,
    tools=[adk_tavily_tool] + github_tools
)


