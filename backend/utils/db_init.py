from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DATE,
    create_engine,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Patients(Base):
    __tablename__ = "patients"
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
    expired_in_months = Column(Integer, nullable=False)


class Diagnostics(Base):
    __tablename__ = "diagnostics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    expired_in_months = Column(Integer, nullable=False)


if __name__ == "__main__":
    engine = create_engine("sqlite:///../database/medical.db")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    objects = [
        Diagnostics(name="Серология", expired_in_months=6),
        Diagnostics(name="BD", expired_in_months=6),
        Diagnostics(name="BL", expired_in_months=6),
        Diagnostics(name="ОАК", expired_in_months=3),
        Diagnostics(name="ОАМ", expired_in_months=3),
        Diagnostics(name="Биохимия", expired_in_months=3),
        Diagnostics(name="Титры", expired_in_months=9999),
        Diagnostics(name="COVID - кровь", expired_in_months=1),
        Diagnostics(name="COVID - мазок", expired_in_months=999),
        Diagnostics(name="Глик.Гемоглобин", expired_in_months=999),
        Diagnostics(name="Онкомаркеры", expired_in_months=999),
        Diagnostics(name="Мокрота на АБ", expired_in_months=999),
        Diagnostics(name="Моча на АБ", expired_in_months=999),
        Diagnostics(name="Я/Г., Стронг", expired_in_months=999),
        Diagnostics(name="Энтеробиоз", expired_in_months=999),
        Diagnostics(name="УЗИ", expired_in_months=999),
        Diagnostics(name="ЭКГ", expired_in_months=3),
        Diagnostics(name="Флюорография", expired_in_months=6),
        Diagnostics(name="Рентген", expired_in_months=999),
        Doctors(name="Терапевт", expired_in_months=6),
        Doctors(name="Невролог", expired_in_months=6),
        Doctors(name="Окулист", expired_in_months=999),
        Doctors(name="Дерматолог", expired_in_months=999),
        Doctors(name="ЛОГ", expired_in_months=999),
        Doctors(name="Хирург", expired_in_months=999),
        Doctors(name="ФТО", expired_in_months=999),
        Doctors(name="Онколог", expired_in_months=999),
        Doctors(name="Фтизиатр", expired_in_months=999),
        Doctors(name="Стоматолог", expired_in_months=999),
        Doctors(name="Инфекционист", expired_in_months=999),
    ]

    session.bulk_save_objects(objects)
    session.commit()
