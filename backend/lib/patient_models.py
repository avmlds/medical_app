from datetime import date
from typing import Optional

from pydantic import BaseModel, validator


class NewPatient(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    birth_date: date
    to_committee: bool
    to_internat: bool


class LinkDiagnostics(BaseModel):
    last_at: date


class LinkDoctors(BaseModel):
    last_at: date
