from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from app.models.career_model import Base
import os
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DATABASE_URL = os.getenv("SQLITE_DATABASE_URL", "sqlite:///./data/database.db")


connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}


load_dotenv()


# DATABASE_URL = "postgresql://appuser:mypassword@localhost:5432/my_project_db"
# primary_engine = create_engine(DATABASE_URL, echo=True)

primary_engine = create_engine(
        DATABASE_URL, 
        echo=True,  # Set to False in production
        connect_args=connect_args 
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=primary_engine)
def init_db():
    Base.metadata.create_all(bind=primary_engine)

def reset_db():
    """Drop and recreate all tables - USE CAREFULLY"""
    try:
        Base.metadata.drop_all(bind=primary_engine)
        Base.metadata.create_all(bind=primary_engine)
        logger.info("Database reset successfully")
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise

def check_db_connection():
    """Check if database connection is working"""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        logger.info("Database connection is working")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False