# presumably this will be the web app you run

import agent

import asyncio
from dotenv import load_dotenv
from google.adk.cli.utils import logs
from google.adk.runners import InMemoryRunner
from google.genai import types

load_dotenv(override=True)
logs.log_to_tmp_folder()

STATE_INITIAL_TOPIC = "initial_topic"
APP_NAME = "doc_writing_app_v3" # New App Name
USER_ID = "dev_user_01"

SESSION_ID_BASE = "loop_exit_tool_session" # New Base Session ID
GEMINI_MODEL = "gemini-2.0-flash"
STATE_CURRENT_DOC = "current_document"
STATE_CRITICISM = "criticism"
# Define the exact phrase the Critic should use to signal completion
COMPLETION_PHRASE = "No major issues found."

runner = InMemoryRunner(agent=agent.root_agent, app_name=APP_NAME)
print(f"InMemoryRunner created for agent '{agent.root_agent.name}'.")

# Interaction function (Modified to show agent names and flow)
async def call_pipeline_async(initial_topic: str, user_id: str, session_id: str):
    print(f"\n--- Starting Iterative Writing Pipeline (Exit Tool) for topic: '{initial_topic}' ---")
    session_service = runner.session_service
    initial_state = {STATE_INITIAL_TOPIC: initial_topic}
    # Explicitly create/check session BEFORE run_async
    session = await session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    if not session:
        print(f"  Session '{session_id}' not found, creating with initial state...")
        session = await session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id, state=initial_state)
        print(f"  Session '{session_id}' created.")
    else:
        print(f"  Session '{session_id}' exists. Resetting state for new run.")
        try:
            # Clear iterative state if reusing session ID
            stored_session = session_service.sessions[APP_NAME][user_id][session_id]
            stored_session.state = {STATE_INITIAL_TOPIC: initial_topic} # Reset state
        except KeyError:
            print("KeyError: Session not found")
            pass # Should not happen if get_session succeeded

    initial_message = types.Content(role='user', parts=[types.Part(text="Start the writing pipeline.")])
    loop_iteration = 0
    pipeline_finished_via_exit = False
    last_known_doc = "No document generated." # Store the last document output

    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=initial_message):
            author_name = event.author or "System"
            is_final = event.is_final_response()
            print(f"  [Event] From: {author_name}, Final: {is_final}")

            # Display output from each main agent when it finishes
            if is_final and event.content and event.content.parts:
                output_text = event.content.parts[0].text.strip()

                if author_name == agent.initial_writer_agent.name:
                    print(f"\n[Initial Draft] By {author_name} ({STATE_CURRENT_DOC}):")
                    print(output_text)
                    last_known_doc = output_text
                elif author_name == agent.critic_agent_in_loop.name:
                    loop_iteration += 1
                    print(f"\n[Loop Iteration {loop_iteration}] Critique by {author_name} ({STATE_CRITICISM}):")
                    print(output_text)
                    print(f"  (Saving to state key '{STATE_CRITICISM}')")
                elif author_name == agent.refiner_agent_in_loop.name:
                    # Only print if it actually refined (didn't call exit_loop)
                    if not event.actions.escalate: # Check if exit wasn't triggered in *this* event's actions
                        print(f"[Loop Iteration {loop_iteration}] Refinement by {author_name} ({STATE_CURRENT_DOC}):")
                        print(output_text)
                        last_known_doc = output_text
                        print(f"  (Overwriting state key '{STATE_CURRENT_DOC}')")

            # Check if the loop was terminated by the exit_loop tool's escalation
            # Note: The escalation action might be attached to the *tool response* event,
            # or the *subsequent model response* if summarization happens.
            # We detect loop termination by seeing if the RefinerAgent calls the tool
            # (indicated by the tool's print statement) or if max iterations hit.
            if event.actions and event.actions.escalate:
                 # We don't know the author for sure here if it's the internal escalation propagation
                 print("\n--- Refinement Loop terminated (Escalation detected) ---")
                 pipeline_finished_via_exit = True
                 # Exit the event processing loop once escalation is detected
                 # as the LoopAgent should stop yielding further internal events.
                 break

            elif event.error_message:
                 print(f"  -> Error from {author_name}: {event.error_message}")
                 break # Stop on error

    except Exception as e: 
        print(f"\n❌ An error occurred during agent execution: {e}")

    # Determine final status based on whether exit_loop was (presumably) called
    if pipeline_finished_via_exit:
        print("\n--- Pipeline Finished (Terminated by exit_loop) ---")
    else:
        print("\n--- Pipeline Finished (Max iterations {agent.refinement_loop.max_iterations} reached or error) ---")

    print(f"Final Document Output:\n{last_known_doc}")

    # Final state retrieval
    final_session_object = await runner.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    print("\n--- Final Session State ---")
    if final_session_object:
        print(final_session_object.state)
    else:
        print("State not found (Final session object could not be retrieved).")
    print("-" * 30)


topic = "a robot developing unexpected emotions"
# topic = "the challenges of communicating with a plant-based alien species"


session_id = f"{SESSION_ID_BASE}_{hash(topic) % 1000}" # Unique session ID



if __name__ == '__main__':
  asyncio.run(call_pipeline_async(topic, user_id=USER_ID, session_id=session_id))
