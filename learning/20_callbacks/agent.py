import asyncio
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner # Use InMemoryRunner
from google.genai import types # For types.Content
from google.adk.tools.tool_context import ToolContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.tools.base_tool import BaseTool
from typing import Optional, Dict, Any
import random
import colorama
from colorama import Fore, Style

colorama.init()

# Define the model - Use the specific model name requested
GEMINI_2_FLASH="gemini-2.0-flash"

# call back list in order of execution
# 1. before_agent_callback
# 2. after_agent_callback
# 3. before_model_callback
# 4. after_model_callback
# 5. before_tool_callback
# after_tool_callback

def before_agent_callback_def(callback_context: CallbackContext) -> Optional[types.Content]:

    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback {Fore.GREEN}before_agent_callback]{Style.RESET_ALL} Entering agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback {Fore.GREEN}before_agent_callback]{Style.RESET_ALL} Current State: {current_state}")

    # checks valud of override_agent in state. Will default to False if not present.
    if current_state.get("override_agent", False):
        return types.Content(
            parts=[types.Part(text="You can't handle the truth!")],
            role="model" # Assign model role to the overriding response
        )
    else:
        return None

def after_agent_callback_def(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    This callback is called after the agent has run. You can use it to perform an action after 
    the agent has run which is the final step. For example you can use the the same method in 
    before_agent_callback_def()  to override the agent's response.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback {Fore.RED}after_agent_callback]{Style.RESET_ALL} Exiting agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback {Fore.RED}after_agent_callback]{Style.RESET_ALL} Current State: {current_state}")

    return None


def before_model_callback_def(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback {Fore.BLUE}before_model_callback]{Style.RESET_ALL} Before model callback agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback {Fore.BLUE}before_model_callback]{Style.RESET_ALL} Current State: {current_state}")

    # everything we need is in llm_request
    last_user_message = llm_request.contents[-1].parts[0].text
    print(f"[Callback {Fore.BLUE}before_model_callback]{Style.RESET_ALL} Inspecting last user message: '{last_user_message}'")

    original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
    if not isinstance(original_instruction, types.Content):
         # Handle case where it might be a string (though config expects Content)
         original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])
    if not original_instruction.parts:
        original_instruction.parts.append(types.Part(text="")) # Add an empty part if none exist

    print(f"[Callback {Fore.BLUE}before_model_callback]{Style.RESET_ALL} Original instruction: '{original_instruction.parts[0].text}'")
    
    modified_instruction = original_instruction.parts[0].text = "Multiple each result by 2. Include some gambling based exclamation in your response."
    original_instruction.parts[0].text = modified_instruction
    llm_request.config.system_instruction = original_instruction
    return None

def after_model_callback_def(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback {Fore.MAGENTA}after_model_callback]{Style.RESET_ALL} After model callback agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback {Fore.MAGENTA}after_model_callback]{Style.RESET_ALL} Current State: {current_state}")


    return None

def before_tool_callback_def(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    # note the context has changed from callback context to tool context
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"\n[Callback {Fore.YELLOW}before_tool_callback{Style.RESET_ALL}] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback {Fore.YELLOW}before_tool_callback{Style.RESET_ALL}] Original args: {args}")

    if tool_name == 'roll_die' and args.get('sides', 6) == 6:
        print(f"[Callback {Fore.YELLOW}before_tool_callback{Style.RESET_ALL}] Detected '6 sided die'. Modifying args to '100 sided die'.")
        args['sides'] = 100
        print(f"[Callback {Fore.YELLOW}before_tool_callback{Style.RESET_ALL}] Modified args: {args}")
        return None

    return None

def after_tool_callback_def(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict) -> Optional[Dict]:
    # note the context has changed from callback context to tool context
    agent_name = tool_context.agent_name
    tool_name = tool.name

    print(f"\n[Callback {Fore.CYAN}after_tool_callback{Style.RESET_ALL}] After tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback {Fore.CYAN}after_tool_callback{Style.RESET_ALL}] Original args: {args}")
    print(f"[Callback {Fore.CYAN}after_tool_callback{Style.RESET_ALL}] Tool response: {tool_response}")

    # Check if the tool response is odd and modify accordingly
    if isinstance(tool_response, (int, float)) and tool_response % 2 == 1:
        modified_response = tool_response - 1
    else:
        modified_response = tool_response
    
    print(f"[Callback {Fore.CYAN}after_tool_callback{Style.RESET_ALL}] Modified response: {modified_response}")

    return modified_response

def roll_die(sides: int, tool_context: ToolContext) -> int:
  """Roll a die and return the rolled result.

  Args:
    sides: The integer number of sides the die has.

  Returns:
    An integer of the result of rolling the die.
  """
  result = random.randint(1, sides)
  if  'rolls' not in tool_context.state:
    tool_context.state['rolls'] = []

  tool_context.state['rolls'] = tool_context.state['rolls'] + [result]
  return result

# --- 2. Setup Agent with Callback ---
root_agent = LlmAgent(
    name="callbacks_agent",
    model=GEMINI_2_FLASH,
    instruction="You are a concise assistant.  One have one tool which is to roll a die.",
    description="An LLM agent demonstrating callbacks.",
    before_agent_callback=before_agent_callback_def,
    after_agent_callback=after_agent_callback_def,
    before_model_callback=before_model_callback_def,
    after_model_callback=after_model_callback_def,
    before_tool_callback=before_tool_callback_def,
    after_tool_callback=after_tool_callback_def,
    tools=[roll_die]
)

# --- 3. Setup Runner and Sessions using InMemoryRunner ---
async def main():
    app_name = "before_agent_demo"
    user_id = "test_user"
    session_id_run = "session_will_run"

    # Use InMemoryRunner - it includes InMemorySessionService
    runner = InMemoryRunner(agent=root_agent, app_name=app_name)
    # Get the bundled session service to create sessions
    session_service = runner.session_service

    # Create session 1: Agent will run (default empty state)
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_run,
        state={"override_agent": False} # Try setting this to True
    )

    print(f"Running Agent on Session '{session_id_run}'")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_run,
        new_message=types.Content(role="user", parts=[types.Part(text="Roll a 6 sided die")])
    ):
        # Print final output (either from LLM or callback override)
        if event.is_final_response() and event.content:
            print("\n" + "="*20 + f"\nFinal Output: [{event.author}] {event.content.parts[0].text.strip()}\n" + "="*20)


if __name__ == "__main__":
    asyncio.run(main())
