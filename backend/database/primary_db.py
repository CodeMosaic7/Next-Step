from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.career_model import Base

DATABASE_URL = "postgresql://appuser:mypassword@localhost:5432/my_project_db"
primary_engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=primary_engine)
def init_db():
    Base.metadata.create_all(bind=primary_engine)