from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATEBASE_URL = "sqlite:///./finance.db"

engine = create_engine(DATEBASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, bind= engine, autocommit = False)

Base = declarative_base()