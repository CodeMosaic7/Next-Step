from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
import dotenv
import os

dotenv.load_dotenv()
class VectorDatabase:
    def __init__(self,embeddings):
        self.pc=Pinecone(api_key=os.getenv("PINECONE_DB"))
        self.index=self.pc.index()
        self.vector_store=PineconeVectorStore(embedding=embeddings, index=self.index)
