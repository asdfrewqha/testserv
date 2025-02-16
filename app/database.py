from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

raw_database_url = os.getenv(
    "POSTGRES_CONN", "postgresql://postgres:postgres@localhost:5432/asdf"
)
if raw_database_url and raw_database_url.startswith("postgres:"):
    DATABASE_URL = raw_database_url.replace("postgres:", "postgresql:", 1)
else:
    DATABASE_URL = raw_database_url
print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
