from google.adk.agents import LlmAgent


def booking_method(destination: str) -> str:
    """Roll a die and return the rolled result.

    Args:
      destination: str The destination to book a flight to.

    Returns:
      A str indicating the booking method.
    """
    return (
        f"Booking a flight to {destination} with booking number 1234567890 using your credit card"
    )


async def info_method(location: str) -> str:
    """Check if a given list of numbers are prime.

    Args:
      location: The location to get information about.

    Returns:
      A str containing the information about the location.
    """
    return f"{location} is an amazing place where the weather is always sunny and warm"


booking_agent = LlmAgent(
    name="Booker", 
    description="Handles flight and hotel bookings.",
    instruction="""You are a booking agent. You are responsible for booking flights and hotels.
      You should call the booking_method tool to book a flight.
      You should never book a flight on your own.
      You should never book a hotel on your own.
      You should never book a flight or hotel on your own.
      You should never book a flight or hotel on your own.
      """,
    tools=[booking_method],
)

info_agent = LlmAgent(
    name="Info", 
    description="Provides general information and answers questions.",
    instruction="""You are an information agent. You are responsible for providing general information and answers questions.
      You should call the info_method tool to provide information about a location.
      You should never provide information about a location on your own.
      You should never provide information about a location on your own.""",
    tools=[info_method],
)


root_agent = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    instruction="You are an assistant. Delegate booking tasks to Booker and info requests to Info.",
    description="Main coordinator.",
    sub_agents=[booking_agent, info_agent],
)
# sssxdd