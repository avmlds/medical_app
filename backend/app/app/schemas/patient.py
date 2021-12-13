import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, root_validator


# Shared properties
class PatientBase(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime.date] = None
    without_documents: Optional[bool] = False
    medical_insurance: Optional[str] = None
    pension_insurance: Optional[str] = None
    address: Optional[str] = None
    passport: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


# Properties to receive via API on creation
class PatientCreate(PatientBase):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime.date] = datetime.date.today()
    without_documents: bool
    medical_insurance: Optional[str] = None
    pension_insurance: Optional[str] = None
    address: Optional[str] = None
    passport: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


# Properties to receive via API on update
class PatientUpdate(PatientBase):
    pass


class PatientInDBBase(PatientBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Patient(PatientInDBBase):
    pass


# Additional properties stored in DB
class PatientInDB(PatientInDBBase):
    pass
