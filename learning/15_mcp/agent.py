from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

def make_map_link(lat: float, lng: float) -> str:
  """Make a link to a Google Maps location.

  Args:
    lat: The latitude of the location.
    lng: The longitude of the location.

  Returns:
    A string of the link to the Google Maps location. The link should be clickable in the UI and open a new browser window.
  """
  return f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"


root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='exif_agent',
    instruction='Help the user fetch exif data for an image.',
    tools=[make_map_link,
            MCPToolset(
                connection_params=StdioServerParameters(
                    command='/Users/graeme/Code/adk/mcp-server-bash-sdk/exifmcpserver.sh',
                    args=[],
                    env={}
                ),
                # You can filter for specific Maps tools if needed:
                # tool_filter=['get_exif']
            )
    ],
)
