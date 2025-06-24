from google.adk.agents import LlmAgent
from toolbox_core import ToolboxSyncClient


toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

# comes from the yaml
google_tools = toolbox.load_toolset('my-toolset')

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='google_tools_agent',
    description='A helpful AI assistant.',
    instruction="""
      You're a helpful hotel assistant. You handle hotel searching, booking and
      cancellations. When the user searches for a hotel, mention it's name, id,
      location and price tier. Always mention hotel ids while performing any
      searches. This is very important for any operations. For any bookings or
      cancellations, please provide the appropriate confirmation. Be sure to
      update checkin or checkout dates if mentioned by the user.
      Don't ask for confirmations from the user.
    """,
    tools=google_tools,
)