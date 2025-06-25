import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import asyncio
from pathlib import Path
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def list_drive_files() -> dict:
    """
    Lists the 10 most recently modified files owned by the user, including
    their web links.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # IMPORTANT: Replace 'credentials.json' with the actual path to your
            # downloaded client secrets file.
            script_dir = Path(__file__).parent
            credentials_file = str(script_dir / "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        token_file = str(script_dir / "token.json")
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API, filtering for files owned by the user and
        # ordering by most recently modified files first.
        results = (
            service.files()
            .list(
                pageSize=10,
                fields="nextPageToken, files(id, name, modifiedTime, owners, webViewLink)",
                orderBy="modifiedTime desc",
                q="'me' in owners",
            )
            .execute()
        )
        items = results.get("files", [])

        if not items:
            return {"message": "No files found."}
        
        files_with_links = [
            {"name": item["name"], "link": item["webViewLink"]} for item in items
        ]
        return {"files": files_with_links}
    except HttpError as error:
        return {"error": f"An error occurred: {error}"}


# --- Agent Configuration ---
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="drive_agent",
    instruction="Your only job is to list Google Drive files. When the user asks for files, you MUST call the `list_drive_files` tool immediately. After the tool returns the file list, format the output as a markdown list where each item is a clickable link to the file. Do not engage in any other conversation.",
    tools=[FunctionTool(list_drive_files)],
)


# --- Agent Runner ---
async def main():
    """Runs the agent."""
    # Note: Ensure you have a 'credentials.json' file in the script's directory.
    script_dir = Path(__file__).parent
    credentials_file = script_dir / "credentials.json"
    if not credentials_file.exists():
        print("ERROR: credentials.json not found.")
        print(f"Please download your OAuth 2.0 Client ID and place it at: {credentials_file}")
        return

    runner = Runner(
        agent=root_agent,
        app_name="drive_agent_app",
        session_service=InMemorySessionService(),
    )
    session = await runner.session_service.create_session(
        app_name="drive_agent_app", user_id="test_user"
    )

    query = "Can you list my files in Google Drive?"
    print(f"User Query: {query}")

    content = Content(parts=[Part(text=query)])
    async for event in runner.run_async(session_id=session.id, new_message=content, user_id="test_user"):
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("---")
            print(f"Agent Response: {final_response}")

if __name__ == "__main__":
    asyncio.run(main())
