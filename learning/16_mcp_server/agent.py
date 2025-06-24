from pathlib import Path
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

script_dir = Path(__file__).parent
PATH_TO_YOUR_MCP_SERVER_SCRIPT = str(script_dir / "server" / "adk_mcp_server.py")
print(f"Path to server script: {PATH_TO_YOUR_MCP_SERVER_SCRIPT}")

toolset = MCPToolset(
            connection_params=StdioServerParameters(
                command='python3', # Command to run your MCP server script
                args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT], # Argument is the path to the script
            )
            # tool_filter=['load_web_page'] # Optional: ensure only specific tools are loaded
        )
        
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='web_reader_mcp_client_agent',
    instruction="Use the 'load_web_page' tool to fetch content from a URL provided by the user.",
    tools=[toolset],
)