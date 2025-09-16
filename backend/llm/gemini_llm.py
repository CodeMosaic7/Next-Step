import os
import dotenv
from langchain.chat_models import init_chat_model
dotenv.load_dotenv()
GEMINI_KEY=os.getenv("GOOGLE_API_KEY")

llm=init_chat_model("google_genai:gemini-2.0-flash")

# For testing purposes
if __name__=="__main__":
    print(llm.invoke("Tell me about Engineer's Day"))