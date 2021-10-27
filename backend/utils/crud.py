from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import POSTGRES_URI

engine = create_engine(POSTGRES_URI)
SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
