from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DATE,
    create_engine,
    UniqueConstraint,
    PrimaryKeyConstraint, Float,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from utils import POSTGRES_URI

Base = declarative_base()


class Commissions(Base):
    __tablename__ = "commissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)


class CommissionsSpecializations(Base):
    __tablename__ = "commissions_specializations"
    __tableargs__ = (
        UniqueConstraint("commission_id", "specialization_id"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    commission_id = Column(Integer, ForeignKey("commissions.id"), nullable=False)
    specialization_id = Column(
        Integer, ForeignKey("specializations.id"), nullable=False
    )
    c_rel = relationship("Commissions")
    s_rel = relationship("Specializations")



class Diagnostics(Base):
    __tablename__ = "diagnostics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    expires_in_days = Column(Integer, nullable=False)


class CommissionsDiagnostics(Base):
    __tablename__ = "commissions_diagnostics"
    __tableargs__ = (
        UniqueConstraint("commission_id", "diagnostic_id"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    commission_id = Column(Integer, ForeignKey("commissions.id"), nullable=False)
    diagnostic_id = Column(
        Integer, ForeignKey("diagnostics.id"), nullable=False
    )
    c_rel = relationship("Commissions")
    s_rel = relationship("Diagnostics")




class Medications(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    medical_name = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    capacity = Column(Float, nullable=False)
    package_amount = Column(Integer, nullable=False)


class Supplies(Base):
    __tablename__ = "supplies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    medical_name = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    capacity = Column(Float, nullable=False)
    package_amount = Column(Integer, nullable=False)


class Patients(Base):
    __tablename__ = "patients"
    __table_args__ = (
        UniqueConstraint(
            "first_name",
            "middle_name",
            "last_name",
            "birth_date",
        ),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)

    birth_date = Column(DATE, nullable=False)
    medical_insurance = Column(String)
    pension_insurance = Column(String)
    address = Column(String)
    passport = Column(String)
    phone = Column(String)
    email = Column(String)
    therapist = Column(Integer, ForeignKey("staff.id"))

    th_rel = relationship("Staff")


class PatientsCommissions(Base):
    __tablename__ = "patients_commissions"
    __tableargs__ = (UniqueConstraint("commission_id", "patient_id"),)
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    commission_id = Column(Integer, ForeignKey("commissions.id"), nullable=False)

    p_relation = relationship("Patients")
    c_relation = relationship("Commissions")


class PatientsAppointments(Base):
    __tablename__ = "patients_appointments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    specialization_id = Column(Integer, ForeignKey("specializations.id"))
    last_at = Column(DATE, default=None)

    patient_relation = relationship("Patients")
    appointment_relation = relationship("Specializations")


class PatientsDiagnostics(Base):
    __tablename__ = "patients_diagnostics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    diagnostic_id = Column(Integer, ForeignKey("diagnostics.id"))
    last_at = Column(DATE, default=None)

    patient_relation = relationship("Patients")
    diagnostics_relation = relationship("Diagnostics")



if __name__ == "__main__":
    engine = create_engine(POSTGRES_URI, echo=True)
    Base.metadata.create_all(engine, checkfirst=True)
    session = sessionmaker(bind=engine)()
    objects = [
        Diagnostics(title="Серология", expires_in_days=6),
        Diagnostics(title="BD", expires_in_days=6),
        Diagnostics(title="BL", expires_in_days=6),
        Diagnostics(title="ОАК", expires_in_days=3),
        Diagnostics(title="ОАМ", expires_in_days=3),
        Diagnostics(title="Биохимия", expires_in_days=3),
        Diagnostics(title="Титры", expires_in_days=9999),
        Diagnostics(title="COVID - кровь", expires_in_days=1),
        Diagnostics(title="COVID - мазок", expires_in_days=999),
        Diagnostics(title="Глик.Гемоглобин", expires_in_days=999),
        Diagnostics(title="Онкомаркеры", expires_in_days=999),
        Diagnostics(title="Мокрота на АБ", expires_in_days=999),
        Diagnostics(title="Моча на АБ", expires_in_days=999),
        Diagnostics(title="Я/Г., Стронг", expires_in_days=999),
        Diagnostics(title="Энтеробиоз", expires_in_days=999),
        Diagnostics(title="УЗИ", expires_in_days=999),
        Diagnostics(title="ЭКГ", expires_in_days=3),
        Diagnostics(title="Флюорография", expires_in_days=6),
        Diagnostics(title="Рентген", expires_in_days=999),
        Specializations(title="Терапевт", expires_in_days=6),
        Specializations(title="Невролог", expires_in_days=6),
        Specializations(title="Окулист", expires_in_days=999),
        Specializations(title="Дерматолог", expires_in_days=999),
        Specializations(title="ЛОГ", expires_in_days=999),
        Specializations(title="Хирург", expires_in_days=999),
        Specializations(title="ФТО", expires_in_days=999),
        Specializations(title="Онколог", expires_in_days=999),
        Specializations(title="Фтизиатр", expires_in_days=999),
        Specializations(title="Стоматолог", expires_in_days=999),
        Specializations(title="Инфекционист", expires_in_days=999),
        MedicalSets(title="Сейф"),
        MedicalSets(title="Скорая помощь"),
        MedicalSets(title="Анафилактический шок"),
        MedicalSets(title="Парентеральные инфекции"),
        MedicalSets(title="Гражданская оборона"),
        Supplies(title="Бинт"),
        Supplies(title="Жгут"),
        Supplies(title="Катетер урологический"),
        Supplies(title="Скарификатор"),
        Supplies(title="Пластырь"),
        Supplies(title="Жгут венозный"),
        Supplies(title="Жгут артериальный"),
        Medications(title="Дротаверин"),
        Medications(title="Парацетамол"),
        Medications(title="Йод"),
        Commissions(title="ВТЭК"),
        Commissions(title="Интернат"),
        Staff(
            first_name="Тест",
            last_name="Тестов",
            middle_name="Тестович",
            phone="9-999-999-99-99",
            personal_phone="9-999-999-99-99",
        ),
    ]

    session.bulk_save_objects(objects)
    session.commit()
