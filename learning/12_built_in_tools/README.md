# Multi-Agent System with Mixed Tool Types in Google ADK

This example demonstrates how to build a robust multi-agent system in the Google ADK (Agent Development Kit). It showcases the "coordinator" or "dispatcher" pattern, where a `root_agent` manages a team of specialized agents.

The key takeaway is how to correctly combine agents that use different types of tools (e.g., a native `VertexAiSearchTool`, a standard `google_search` function, and a `BuiltInCodeExecutor`) by using the `AgentTool` wrapper. This pattern avoids the `400 INVALID_ARGUMENT: Multiple tools are supported only when they are all search tools` error.

## Architecture

The system is composed of:
1.  A **`root_agent`**: Acts as a team coordinator. It analyzes the user's request and delegates the task to the appropriate specialist agent.
2.  Three **specialist agents**:
    -   `basic_search_agent`: Uses the built-in `google_search` tool to search the internet.
    -   `doc_qa_agent`: Uses the `VertexAiSearchTool` to answer questions from a specific private document datastore.
    -   `calculator_agent`: Uses the `BuiltInCodeExecutor` to perform calculations.
3.  The **`AgentTool` Wrapper**: Each specialist agent is wrapped in an `AgentTool` before being given to the `root_agent`. This abstracts their internal toolsets and presents a uniform "function tool" interface to the coordinator, resolving potential conflicts between different tool types.

## Prerequisites

- Python 3.9+
- Google Cloud project with Vertex AI Search enabled
- A Vertex AI Search datastore created (note the region and resource name format)
- `gcloud` CLI installed and authenticated

## Environment Setup

1. **Install dependencies:** The ADK is the primary dependency.
   ```sh
   pip install google-adk
   ```

2. **Set environment variables:** Create a `.env` file in this directory or set them in your shell.
   ```sh
   # Required for the doc_qa_agent
   export GOOGLE_GENAI_USE_VERTEXAI=True
   export GOOGLE_CLOUD_PROJECT=<YOUR_PROJECT_ID>
   export GOOGLE_CLOUD_LOCATION=<YOUR_REGION>  # e.g., us-central1

   # Do NOT set GOOGLE_API_KEY when using Vertex AI
   ```
   The included `agent.py` script will automatically load the `.env` file.

3. **Authenticate:**
   ```sh
   gcloud auth application-default login
   ```

## Usage

Run the agent using the ADK's built-in web interface. From the parent directory (`learning/`), run:

```sh
adk web
```

- Open the provided URL (e.g., `http://localhost:8000`).
- Select `12_built_in_tools` from the agent dropdown menu.
- You can now chat with the `root_agent`.

## Example Queries

Try asking questions that target different specialists:

- **To trigger the `basic_search_agent`:**
  > "Who is the current prime minister of New Zealand?"

- **To trigger the `doc_qa_agent` (using the example datastore):**
  > "What is the sentence for 'Obtaining by deception'?"

- **To trigger the `calculator_agent`:**
  > "What is 42 * 119?"

## Troubleshooting

- **`400 INVALID_ARGUMENT: Multiple tools are supported only when they are all search tools.`**
  - **Cause:** This error occurs when an agent is given a mix of native search tools (`VertexAiSearchTool`) and standard function tools. This can happen if you pass agents with different tool types to the `sub_agents` parameter of a parent agent.
  - **Solution:** Do not use the `sub_agents` parameter in this scenario. Instead, wrap each specialist agent in an `AgentTool` and pass the list of wrapped tools to the parent agent's `tools` parameter, as demonstrated in this example.

- **`401 UNAUTHENTICATED`:**
  - Make sure you have authenticated using `gcloud auth application-default login`.
  - Ensure you have **not** set a `GOOGLE_API_KEY` when `GOOGLE_GENAI_USE_VERTEXAI` is `True`. The script attempts to handle this, but manual setup can interfere.

- **`400 INVALID_ARGUMENT: Invalid Vertex AI datastore resource name`:**
  - Double-check the `YOUR_DATASTORE_ID` variable in `agent.py`. It must be the full resource name, including the project ID and location.

---

For more information, see:
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Vertex AI Search Documentation](https://cloud.google.com/vertex-ai/docs/search) 