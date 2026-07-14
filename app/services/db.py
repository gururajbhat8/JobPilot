
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models.db_models import Base

load_dotenv()

# 1. connection string we saved in .env
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. The Engine is the core connection to Postgres
engine = create_engine(DATABASE_URL) 

# 3. SessionLocal is a factory that creates new database sessions for us
SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind= engine)

def init_db():
    # This magically looks at our db_models.py and creates the tables in Postgres if they don't exist!
    Base.metadata.create_all(bind=engine)


def get_db():
    # This gives a temporary database session to our API, and ensures it closes when done.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
