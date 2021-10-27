from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DATE,
    create_engine,
    UniqueConstraint,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from utils import POSTGRES_URI

Base = declarative_base()


class Patients(Base):
    __tablename__ = "patients"
    __table_args__ = (
        UniqueConstraint(
            "first_name",
            "middle_name",
            "last_name",
            "birth_date",
            "to_committee",
            "to_internat",
        ),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)

    birth_date = Column(DATE, nullable=False)

    to_committee = Column(Boolean, nullable=False, default=False)
    to_internat = Column(Boolean, nullable=False, default=False)


class PatientDoctors(Base):
    __tablename__ = "p_doctors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    last_at = Column(DATE, default=None)

    patient_relation = relationship("Patients")
    doctors_relation = relationship("Doctors")


class PatientDiagnostics(Base):
    __tablename__ = "p_diagnostics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    diagnostic_id = Column(Integer, ForeignKey("diagnostics.id"))
    last_at = Column(DATE, default=None)

    patient_relation = relationship("Patients")
    diagnostics_relation = relationship("Diagnostics")


class Doctors(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    expires_in_months = Column(Integer, nullable=False)


class Diagnostics(Base):
    __tablename__ = "diagnostics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    expires_in_months = Column(Integer, nullable=False)


if __name__ == "__main__":
    engine = create_engine(POSTGRES_URI)
    Base.metadata.create_all(engine, checkfirst=True)
    session = sessionmaker(bind=engine)()
    objects = [
        Diagnostics(name="Серология", expires_in_months=6),
        Diagnostics(name="BD", expires_in_months=6),
        Diagnostics(name="BL", expires_in_months=6),
        Diagnostics(name="ОАК", expires_in_months=3),
        Diagnostics(name="ОАМ", expires_in_months=3),
        Diagnostics(name="Биохимия", expires_in_months=3),
        Diagnostics(name="Титры", expires_in_months=9999),
        Diagnostics(name="COVID - кровь", expires_in_months=1),
        Diagnostics(name="COVID - мазок", expires_in_months=999),
        Diagnostics(name="Глик.Гемоглобин", expires_in_months=999),
        Diagnostics(name="Онкомаркеры", expires_in_months=999),
        Diagnostics(name="Мокрота на АБ", expires_in_months=999),
        Diagnostics(name="Моча на АБ", expires_in_months=999),
        Diagnostics(name="Я/Г., Стронг", expires_in_months=999),
        Diagnostics(name="Энтеробиоз", expires_in_months=999),
        Diagnostics(name="УЗИ", expires_in_months=999),
        Diagnostics(name="ЭКГ", expires_in_months=3),
        Diagnostics(name="Флюорография", expires_in_months=6),
        Diagnostics(name="Рентген", expires_in_months=999),
        Doctors(name="Терапевт", expires_in_months=6),
        Doctors(name="Невролог", expires_in_months=6),
        Doctors(name="Окулист", expires_in_months=999),
        Doctors(name="Дерматолог", expires_in_months=999),
        Doctors(name="ЛОГ", expires_in_months=999),
        Doctors(name="Хирург", expires_in_months=999),
        Doctors(name="ФТО", expires_in_months=999),
        Doctors(name="Онколог", expires_in_months=999),
        Doctors(name="Фтизиатр", expires_in_months=999),
        Doctors(name="Стоматолог", expires_in_months=999),
        Doctors(name="Инфекционист", expires_in_months=999),
    ]

    session.bulk_save_objects(objects)
    session.commit()
