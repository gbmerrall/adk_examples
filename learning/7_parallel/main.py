import agent
from google.adk.runners import InMemoryRunner
from google.genai import types
import asyncio
import traceback

APP_NAME = "parallel_research_app"
USER_ID = "research_user_01"
SESSION_ID = "parallel_research_session_with_merge"
GEMINI_MODEL = "gemini-2.0-flash"


# Use InMemoryRunner: Ideal for quick prototyping and local testing
runner = InMemoryRunner(agent=agent.root_agent, app_name=APP_NAME)
print(f"InMemoryRunner created for agent '{agent.root_agent.name}'.")

# We still need access to the session service (bundled in InMemoryRunner)
# to create the session instance for the run.
session_service = runner.session_service

async def call_sequential_pipeline(query: str, user_id: str, session_id: str):
    """
    Helper async function to call the sequential agent pipeline.
    Prints intermediate results from parallel agents and the final merged response.
    """
    print(f"\n--- Running Research & Synthesis Pipeline for query: '{query}' ---")
    # Create session before running the pipeline
    await session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    print(f"Session '{session_id}' created for direct run.")
    
    # The initial query mainly triggers the pipeline; the research topics are fixed in the agents for this example.
    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = None
    # Keep track of which researchers have reported
    researcher_outputs = {}
    researcher_names = {"RenewableEnergyResearcher", "EVResearcher", "CarbonCaptureResearcher"}
    merger_agent_name = "SynthesisAgent" # Name of the final agent in sequence

    print("Starting pipeline...")
    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            author_name = event.author or "System"
            is_final = event.is_final_response()
            print(f"  [Event] From: {author_name}, Final: {is_final}") # Basic event logging

            # Check if it's a final response from one of the researcher agents
            if is_final and author_name in researcher_names and event.content and event.content.parts:
                researcher_output = event.content.parts[0].text.strip()
                if author_name not in researcher_outputs: # Print only once per researcher
                    print(f"    -> Intermediate Result from {author_name}: {researcher_output}")
                    researcher_outputs[author_name] = researcher_output

            # Check if it's the final response from the merger agent (the last agent in the sequence)
            elif is_final and author_name == merger_agent_name and event.content and event.content.parts:
                 final_response_text = event.content.parts[0].text.strip()
                 print(f"\n<<< Final Synthesized Response (from {author_name}):\n{final_response_text}")
                 # Since this is the last agent in the sequence, we can break after its final response
                 break

            elif event.is_error():
                 print(f"  -> Error from {author_name}: {event.error_message}")

        if final_response_text is None:
             print("<<< Pipeline finished but did not produce the expected final text response from the SynthesisAgent.")

    except Exception as e:
        print(f"\n❌ An error occurred during agent execution: {e}")
        traceback.print_exc() 


initial_trigger_query = "Summarize recent circular and sustainable economy advancements especially in tech."


if __name__ == '__main__':
  asyncio.run(call_sequential_pipeline(initial_trigger_query, user_id=USER_ID, session_id=SESSION_ID))