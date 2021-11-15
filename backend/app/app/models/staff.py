from sqlalchemy import Column, ForeignKey, Integer, String, Float, DATE, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


# ------------ Specializations and staff


class Specializations(Base):
    __tablename__ = "specializations"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False, unique=True)


class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, autoincrement=True)

    specialization_id = Column(Integer, ForeignKey("specializations.id"))
    department_id = Column(Integer, ForeignKey("hospital_departments.id"))

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)

    email = Column(String, default=None)
    phone = Column(String, default=None)

    # production_mode - nullable=False)
    address = Column(String)
    personal_phone = Column(String)

    tax_number = Column(String)
    birth_date = Column(DATE)

    medical_insurance = Column(String)
    pension_insurance = Column(String)

    passport_series = Column(String)
    passport_number = Column(String)

    current_salary = Column(Float)

    employed_at = Column(DATE)
    dismissed_at = Column(DATE)

    notes = Column(Text)

    sp_rel = relationship("Specializations")
    staff_dep_rel = relationship("HospitalDepartments", foreign_keys=[department_id])
