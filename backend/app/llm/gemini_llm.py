import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

dotenv.load_dotenv()

# Get the API key
GEMINI_KEY = os.getenv("GOOGLE_API_KEY")

class LLM_initialise:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=GEMINI_KEY,
            temperature=0.7,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
    
    def get_llm(self):
        return self.llm
