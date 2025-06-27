import os
import sys
from openai import OpenAI
from typing import Optional, List

def test_openai_api(api_key: Optional[str] = None) -> bool:
    """
    Test the OpenAI API key by making a simple completion request.
    
    Args:
        api_key (Optional[str]): The OpenAI API key. If None, will try to get from environment.
        
    Returns:
        bool: True if the API call was successful, False otherwise.
    """
    try:
        # Use provided API key or get from environment
        client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        
        # Make a simple test request
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'API test successful' if you can read this."}],
            max_tokens=10
        )
        
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"Error testing API: {e}", file=sys.stderr)
        return False

def list_available_models(api_key: Optional[str] = None) -> List[str]:
    """
    List all available models from the OpenAI API.
    
    Args:
        api_key (Optional[str]): The OpenAI API key. If None, will try to get from environment.
        
    Returns:
        List[str]: List of available model IDs
    """
    try:
        client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        models = client.models.list()
        
        print("\nAvailable Models:")
        print("-" * 50)
        for model in models.data:
            print(f"ID: {model.id}")
            print(f"Created: {model.created}")
            print(f"Owned by: {model.owned_by}")
            print("-" * 50)
            
        return [model.id for model in models.data]
        
    except Exception as e:
        print(f"Error listing models: {e}", file=sys.stderr)
        return []

if __name__ == "__main__":
    # You can either set OPENAI_API_KEY in your environment
    # or pass it as a command line argument
    
    if test_openai_api():
        print("API test completed successfully!")
        # List available models after successful API test
        # list_available_models(api_key)
    else:
        print("API test failed. Please check your API key and try again.")
