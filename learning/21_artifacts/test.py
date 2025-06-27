import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types
import agent

async def main():
    app_name = 'pdf_app'
    user_id = 'user1'
    session_id = 'session1'
    
    # Prompt user for text
    text = input("Enter the text to generate a PDF: ")

    # Set up services
    artifact_service = InMemoryArtifactService()
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent.root_agent,
        app_name=app_name,
        session_service=session_service,
        artifact_service=artifact_service,
    )

    # Create session
    await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id)

    # Run the agent
    content = types.Content(role='user', parts=[types.Part(text=f"generate a PDF: {text}")])
    filename = None
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response() and event.content and event.content.parts:
            print(f"Agent: {event.content.parts[0].text}")
        
        # Try to extract filename from tool response if present
        if event.get_function_responses():
            response = event.get_function_responses()[0]
            print(response)
            if isinstance(response.response, dict) and 'filename' in response.response:
                filename = response.response['filename']
    
    if not filename:
        print("No PDF filename returned by the agent.")
        return

    # Retrieve the artifact (PDF)
    artifact = await artifact_service.load_artifact(
        app_name=app_name, user_id=user_id, session_id=session_id, filename=filename
    )
    if artifact and artifact.inline_data:
        with open(filename, 'wb') as f:
            f.write(artifact.inline_data.data)
        print(f"PDF saved as {filename}")
    else:
        print("Failed to retrieve the PDF artifact.")

if __name__ == "__main__":
    asyncio.run(main())