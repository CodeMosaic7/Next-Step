from sqlalchemy import create_engine

DATABASE_URL = "postgresql://appuser:mypassword@localhost:5432/my_project_db"
primary_engine = create_engine(DATABASE_URL, echo=True)