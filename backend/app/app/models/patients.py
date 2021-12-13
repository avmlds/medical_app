from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    DATE,
    Boolean,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# ------------ Patients, medical cards, prescriptions, diagnoses, diseases and procedures


class Patients(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)

    birth_date = Column(DATE, server_default=func.now())
    without_documents = Column(Boolean, default=False)

    medical_insurance = Column(String)
    pension_insurance = Column(String)

    address = Column(String)
    passport = Column(String)
    phone = Column(String)
    email = Column(String)


class Diseases(Base):
    """Table for storing diseases classifications
    based on DSM/ICD"""

    __tablename__ = "diseases"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    source = Column(Integer, nullable=False)
    is_actual = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class Diagnoses(Base):
    """Table that connects multiple diseases to medical records"""

    __tablename__ = "diagnoses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    record_id = Column(Integer, ForeignKey("medical_records.id"))


class Procedures(Base):
    """Table with procedures for patients"""

    __tablename__ = "procedures"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class ProceduresRecords(Base):
    """Table for connections between medical
    manipulations/procedures and medical records
    files will be stored in a key/value storage,
    like minio / S3 etc.
    """

    __tablename__ = "procedures_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey("medical_records.id"))
    procedure_id = Column(Integer, ForeignKey("procedures.id"))
    files = Column(JSONB)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class MedicalRecords(Base):
    """Table with medical records about patients,
    their manipulations, diagnoses and prescriptions"""

    __tablename__ = "medical_records"
    id = Column(Integer, primary_key=True, autoincrement=True)

    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    patient_claims = Column(Text)
    specialists_notes = Column(Text, nullable=False)

    patient_instructions = Column(Text)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    staff_secret = Column(String, nullable=False)
    hash_sum = Column(String, nullable=False)

    patient_rel = relationship("Patients")
    staff_rel = relationship("Staff")


class PatientAppointments(Base):
    """Table for storing appointments with medical staff"""

    __tablename__ = "patient_appointments"
    id = Column(Integer, primary_key=True, autoincrement=True)

    record_id = Column(Integer, ForeignKey("medical_records.id"))
    appointment_with = Column(Integer, ForeignKey("staff.id"))

    scheduled_at = Column(DateTime, nullable=False)

    valid_until = Column(DateTime, nullable=False)
    took_place = Column(Boolean, nullable=False, default=False)

    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, onupdate=func.now())

    record_rel = relationship("MedicalRecords")
    staff_rel = relationship("Staff")


class PatientPrescriptions(Base):
    """Table for storing prescriptions for patients"""

    __tablename__ = "patient_prescriptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey("medical_records.id"))
    medicine_id = Column(Integer, ForeignKey("medical_items.id"))
    medication_schedule = Column(String, nullable=False)

    record_rel = relationship("MedicalRecords")
    medicine_rel = relationship("MedicalItems")
