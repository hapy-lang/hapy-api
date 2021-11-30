from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV").strip()
DATABASE_URL = os.getenv(f"{ENV}_DB_URL").strip()

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
