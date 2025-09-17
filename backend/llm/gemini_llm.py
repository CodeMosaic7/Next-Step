import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

dotenv.load_dotenv()

# Get the API key
GEMINI_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM with proper configuration
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",  # Use the correct model name
    google_api_key=GEMINI_KEY,
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# For testing purposes
if __name__ == "__main__":
    try:
        response = llm.invoke("Tell me about Engineer's Day")
        print("LLM Response:")
        print(response.content)
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        print("Please check:")
        print("1. Your GOOGLE_API_KEY is set correctly in .env file")
        print("2. You have installed: pip install langchain-google-genai")
        print("3. Your API key has proper permissions")