from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# ------------ Administrative structure


class DepartmentTypes(Base):
    """Types of medical departments classified by profile
    such as surgical or intensive care or
    advisory or inpatient"""

    __tablename__ = "department_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


class OfficeTypes(Base):
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
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    department_type = Column(Integer, ForeignKey("department_types.id"))
    title = Column(String, nullable=False)

    hospital_rel = relationship("Hospitals", foreign_keys=[hospital_id])
    dep_type_rel = relationship("DepartmentTypes", foreign_keys=[department_type])


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
