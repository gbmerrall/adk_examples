# LiteLLM is an easy way to swap models. You can also import a provider directly if there's support
# which is only Anthropic at this stage

# You can also use a local model with LiteLLM but you need to install the model first.
# e.g. ollama pull deepseek-r1:1.5b
# they may not support tool calling. e.g. deepseek-r1:1.5b does not support tool calling.
# See https://ollama.com/search?c=tools

import random

from google.adk import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.models.lite_llm import LiteLlm
from google.genai import types


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


async def check_prime(nums: list[int]) -> str:
  """Check if a given list of numbers are prime.

  Args:
    nums: The list of numbers to check.

  Returns:
    A str indicating which number is prime.
  """
  primes = set()
  for number in nums:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      'No prime numbers found.'
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )


root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='hello_world_agent',
    description=(
        'hello world agent that can roll a dice of any number of sides and check prime'
        ' numbers.'
    ),
    instruction="""
      You are an agent that can use tools.
      - To roll a die, call the `roll_die(sides: int)` tool.
      - To check for prime numbers, call `check_prime(nums: list[int])`.
      Only call the tools when requested.
    """,
    tools=[
        roll_die,
        check_prime,
    ],
)