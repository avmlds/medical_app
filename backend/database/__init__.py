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

# ------------ Specializations and staff


class Specializations(Base):
    __tablename__ = "specializations"
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    dep_rel = relationship("HospitalDepartments")


# ------------ Administrative structure


class DepartmentTypes(Base):
    """Types of medical departments classified by profile
    such as surgical or intensive care or
    advisory or inpatient"""

    __tablename__ = "department_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


class OfficeType(Base):
    """Types of medical offices classified by purpose,
    such as department warehouse,
    doctor's office, or laboratory"""

    __tablename__ = "office_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


class WardTypes(Base):
    """Types of medical wards classified by purpose,
    for example a regular ward or an intensive care ward"""

    __tablename__ = "ward_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


class Hospitals(Base):
    """hospital"""

    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    address = Column(String, nullable=False)


class HospitalDepartments(Base):
    """hospital departments"""

    __tablename__ = "hospital_departments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chief_id = Column(Integer, ForeignKey("staff.id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    department_type = Column(Integer, ForeignKey("department_types.id"))
    title = Column(String, nullable=False)

    hospital_rel = relationship("Hospitals")
    dep_type_rel = relationship("DepartmentTypes")


class DepartmentOffices(Base):
    """doctors' offices"""

    __tablename__ = "department_offices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    office_type = Column(Integer, ForeignKey("office_types.id"))
    department_id = Column(Integer, ForeignKey("hospital_departments.id"))

    office_type_rel = relationship("OfficeTypes")
    dep_rel = relationship("HospitalDepartments")


class DepartmentWards(Base):
    """patient room"""

    __tablename__ = "department_wards"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    ward_type = Column(Integer, ForeignKey("ward_types.id"))
    department_id = Column(Integer, ForeignKey("hospital_departments.id"))

    ward_type_rel = relationship("WardTypes")
    dep_rel = relationship("HospitalDepartments")


class WardPlaces(Base):
    """hospital bed/place assigned to the patient"""

    __tablename__ = "ward_places"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    ward_id = Column(Integer, ForeignKey("department_wards.id"))

    ward_rel = relationship("DepartmentWards")


class OfficeStaff(Base):
    """hospital staff, assigned to office"""

    __tablename__ = "office_staff"
    __tableargs__ = (UniqueConstraint("office_id", "staff_id"),)
    id = Column(Integer, primary_key=True, autoincrement=True)

    office_id = Column(Integer, ForeignKey("staff.id"))
    staff_id = Column(Integer, ForeignKey("department_offices.id"))

    office_rel = relationship("DepartmentOffices")
    staff_rel = relationship("Staff")


# ------------ Hospital warehouse and transitions between warehouses


class WarehouseTypes(Base):
    """Table with warehouse types, e.g. medical, clothes,
    trash(for items that were discontinued and sent to trash) etc."""

    __tablename__ = "warehouse_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    purpose = Column(String, nullable=False)


class MedicalItems(Base):
    """Various Medical items, from pills to scissors"""

    __tablename__ = "medical_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    medical_name = Column(String)
    unit = Column(String, nullable=False)
    capacity = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)


class MedicalCompositions(Base):
    """Compositions of medical items, Anti-HIV,
    Emergency medical set, etc."""

    __tablename__ = "medical_compositions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    composite_item_id = Column(Integer, ForeignKey("medical_items.id"))
    consists_from = Column(Integer, ForeignKey("medical_items.id"))
    quantity = Column(Float, nullable=False, default=1)

    item_kit_relation = relationship("MedicalItems")


class WareHouses(Base):
    """Warehouses for departments and hospitals.
    Nullable department id and not null hospital id means
    that it is a central hospital warehouse"""

    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, autoincrement=True)

    warehouse_type = Column(Integer, ForeignKey("warehouse_types.id"), nullable=False)

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    department_id = Column(
        Integer, ForeignKey("hospital_departments.id"), nullable=True
    )

    hospital_refs = relationship("Hospitals")
    warehouse_type_refs = relationship("WarehouseTypes")
    department_refs = relationship("HospitalDepartments")


class WareHouseItems(Base):
    """Class for storing medical items in any warehouse"""

    __tablename__ = "warehouse_items"
    id = Column(Integer, primary_key=True, autoincrement=True)

    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))

    item_id = Column(Integer, ForeignKey("medical_items.id"))
    quantity = Column(Float, nullable=False, default=0)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    wh_rel = relationship("WareHouses")
    med_items_rel = relationship("MedicalItems")


class WarehousesTransitions(Base):
    """Class that describes transitions
    between warehouses"""

    __tablename__ = "warehouses_transitions"
    id = Column(Integer, primary_key=True, autoincrement=True)

    current_warehouse = Column(Integer, ForeignKey("warehouses.id"))
    target_warehouse = Column(Integer, ForeignKey("warehouses.id"))

    item = Column(Integer, ForeignKey("warehouse_items.id"))
    quantity = Column(Float, nullable=False, default=0)

    staff = Column(Integer, ForeignKey("staff.id"))
    target_staff = Column(Integer, ForeignKey("staff.id"))

    created_at = Column(DateTime, nullable=False)

    staff_rel = relationship("Staff")
    wh_rel = relationship("WareHouses")
    med_items_rel = relationship("WareHouseItems")


# ------------ Patients, medical cards, prescriptions, diagnoses, diseases and procedures


class Patients(Base):
    __tablename__ = "patients"
    __table_args__ = (
        UniqueConstraint(
            "first_name",
            "middle_name",
            "last_name",
            "birth_date",
            "medical_insurance",
        ),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)

    birth_date = Column(DATE, nullable=False)
    medical_insurance = Column(String, nullable=False)
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
    created_at = Column(DateTime, nullable=False)


class Diagnoses(Base):
    """Table that connects multiple diseases to medical records"""

    __tablename__ = "diagnoses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    record_id = Column(Integer, ForeignKey("medical_records.id"))


class Procedures(Base):
    """Table that connects multiple diseases to medical records"""

    __tablename__ = "procedures"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


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
    created_at = Column(DateTime, nullable=False)


class MedicalRecords(Base):

    __tablename__ = "medical_records"
    id = Column(Integer, primary_key=True, autoincrement=True)

    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    patient_claims = Column(Text)
    specialists_notes = Column(Text, nullable=False)

    diagnoses = Column(Integer, ForeignKey("diagnoses.id"), nullable=True)

    patient_instructions = Column(Text)

    created_at = Column(DateTime, nullable=False)
    staff_secret = Column(String, nullable=False)
    hash_sum = Column(String, nullable=False)


class PatientAppointments(Base):
    """Table for storing prescriptions for patients"""

    __tablename__ = "patient_appointments"
    id = Column(Integer, primary_key=True, autoincrement=True)

    record_id = Column(Integer, ForeignKey("medical_records.id"))
    appointment_with = Column(Integer, ForeignKey("staff.id"))

    scheduled_at = Column(DateTime, nullable=False)

    valid_until = Column(DateTime, nullable=False)
    took_place = Column(Boolean, nullable=False, default=False)

    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

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


engine = create_engine(POSTGRES_URI, echo=True)
Base.metadata.create_all(engine, checkfirst=True)
