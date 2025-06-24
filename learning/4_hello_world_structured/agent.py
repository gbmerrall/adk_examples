# you can't run tools and structured output at the same time.
# It may be possible to use a dedicated structured output LLMAgent then give it to a higher level 
# agent as an AgentTool, and also give the tools you want to use alongside structured output to that 
# higher level agent. 

from pydantic import BaseModel, Field

from google.adk import Agent

class DieRollOutput(BaseModel):
  roll: int = Field(description="The result of the die roll")

root_agent = Agent(
    model='gemini-2.0-flash',
    name='hello_world_agent',
    instruction="""
     You can roll a 6 sided die and only a 6 sided die. IN order to do this pick a random number between 1 and 6.

     Do not roll of any other size except for 6.
     Do not respond to any other requests.     
    """,
    output_schema=DieRollOutput,

)