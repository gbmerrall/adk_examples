# Google Drive OAuth Agent Example (Updated)

This example demonstrates how to build a Google Agent Development Kit (ADK) agent that uses the standard Google Authentication Libraries to access a user's Google Drive.

This version uses the recommended `InstalledAppFlow` from the `google-auth-oauthlib` library, which is the standard way to handle user authentication for desktop and command-line applications.

## How it Works

The authentication logic is now self-contained within the `list_drive_files` tool function:

1.  **Path-Aware Logic**: The script is now path-aware. It looks for both `credentials.json` and the generated `token.json` file in the same directory where the `agent.py` script itself is located. This makes the script more robust, as it can be run from any location.
2.  **Token Storage**: The script looks for the `token.json` file to find stored user credentials, avoiding the need to log in every time.
3.  **First-Time Auth**: If `token.json` is missing, invalid, or expired, the script triggers the `InstalledAppFlow`.
4.  **Browser-Based Flow**: The `flow.run_local_server()` method automatically starts a temporary, local web server and opens the user's default web browser to the Google Account consent screen.
5.  **User Consent**: The user logs into their Google Account and grants the requested permissions (in this case, to view Google Drive files).
6.  **Credential Storage**: After consent is given, the library automatically handles the token exchange and saves the new credentials into `token.json` for future use.
7.  **API Call**: With valid credentials, the tool function then proceeds to call the Google Drive API to fetch the 10 most recently modified files owned by the user, along with their web URLs.

This approach is more robust and aligns with Google's official best practices for Python applications.

## Setup Instructions

### 1. Install Dependencies

If you haven't already, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Get Google OAuth 2.0 Credentials (`credentials.json`)

To run this agent, you need to download an OAuth 2.0 Client ID JSON file from the Google Cloud Console.

1.  **Enable the Google Drive API**:
    *   Go to the [Google Cloud Console API Library](https://console.cloud.google.com/apis/library).
    *   Ensure you have a project selected.
    *   Search for "Google Drive API" and click **Enable**.

2.  **Configure the OAuth Consent Screen**:
    *   Go to the [OAuth consent screen page](https://console.cloud.google.com/apis/credentials/consent).
    *   Choose **External** for the User Type and click **Create**.
    *   Fill in the required app information (app name, user support email, developer contact).
    *   On the "Scopes" and "Test users" pages, you can click **Save and Continue** for now. You will add test users later.
    *   Add your own Google email account to the list of **Test users**. The app will only work for these users while it's in "testing" mode.

3.  **Create OAuth Credentials**:
    *   Go to the [Credentials page](https://console.cloud.google.com/apis/credentials).
    *   Click **+ CREATE CREDENTIALS** and select **OAuth client ID**.
    *   For the **Application type**, select **Desktop app**.
    *   Give it a name (e.g., "ADK Drive CLI").
    *   Click **Create**.

4.  **Download the JSON File**:
    *   A window will pop up showing your Client ID and Secret. **Do not copy these**.
    *   On the right side of your newly created "Desktop application" credential, click the **Download JSON** icon.
    *   Rename the downloaded file to `credentials.json`.

### 3. Place the Credentials File

Move the `credentials.json` file into the `learning/19_oauth/` directory, alongside `agent.py`.

## Run the Agent

Once your `credentials.json` file is in place, run the agent from the root of the `adk_examples` directory:

```bash
python learning/19_oauth/agent.py
```

The first time you run it, your web browser will open and ask for permission to access your Google Drive. After you approve, the agent will respond with a clickable markdown list of your 10 most recently modified files. Subsequent runs will use the saved `token.json` and will not require you to log in again. 