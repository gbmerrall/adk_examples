from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.agents import LlmAgent
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with the URL where your FastAPI app is running
FASTAPI_APP_BASE_URL = "http://localhost:8080" 

# --- ADK Authentication Setup ---
# This API_KEY must match the one you set in your FastAPI app
ADK_API_KEY_STRING = os.getenv("FASTAPI_API_KEY", "your-secret-fastapi-key")  # Get from env or use placeholder
ADK_API_KEY_HEADER_NAME = "X-API-Key"  # This matches API_KEY_NAME in FastAPI

auth_scheme, auth_credential = token_to_scheme_credential(
   "apikey", "header", ADK_API_KEY_HEADER_NAME, ADK_API_KEY_STRING
)

try:
    response = requests.get(f"{FASTAPI_APP_BASE_URL}/openapi.json")
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    fastapi_openapi_spec = response.json()
    
    print(f"Successfully fetched OpenAPI spec from FastAPI at {FASTAPI_APP_BASE_URL}")
except requests.exceptions.RequestException as e:
    print(f"Error fetching OpenAPI spec: {e}")
    print(f"Ensure your FastAPI app is running at {FASTAPI_APP_BASE_URL}")
    print("You can start it with: fastapi run main.py --host 0.0.0.0 --port 8080")
    fastapi_openapi_spec = None  # Handle the case where spec cannot be fetched

# Only create the toolset if we have a valid OpenAPI spec
if fastapi_openapi_spec is not None:
    sample_api_toolset = OpenAPIToolset(
        spec_dict=fastapi_openapi_spec,  # Provide the spec as a dictionary
        auth_scheme=auth_scheme,
        auth_credential=auth_credential,
    )
    
    # --- Create the Agent ---
    root_agent = LlmAgent(
           name="pet_manager",
           model="gemini-2.0-flash",  # Or your preferred model
           instruction=f"""You are a pet store manager. You can use the sample_api_toolset 
            Use the pet_store_api at {FASTAPI_APP_BASE_URL} to list, create, and manage pets.""",
           tools=[sample_api_toolset]  # This will expose list_pets and create_pet as tools
    )
else:
    print("Cannot create agent without OpenAPI spec. Please ensure your FastAPI server is running.")
    root_agent = None