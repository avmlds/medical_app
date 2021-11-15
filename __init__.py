import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DATE,
    Float,
    Text,
    create_engine,
    DateTime,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from utils import POSTGRES_URI

Base = declarative_base()


engine = create_engine(POSTGRES_URI, echo=True)
Base.metadata.create_all(engine, checkfirst=True)
