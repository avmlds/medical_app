from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import SQLITE_STRING_MAIN

engine = create_engine(SQLITE_STRING_MAIN, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
