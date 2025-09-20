from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.career_model import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("SQLITE_DATABASE_URL")
# DATABASE_URL = "postgresql://appuser:mypassword@localhost:5432/my_project_db"
# primary_engine = create_engine(DATABASE_URL, echo=True)

primary_engine = create_engine(
        DATABASE_URL, 
        echo=True,  # Set to False in production
        connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=primary_engine)
def init_db():
    Base.metadata.create_all(bind=primary_engine)