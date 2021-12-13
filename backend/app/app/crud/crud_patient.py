import uuid

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.patients import Patients
from app.schemas import PatientCreate, PatientUpdate


def create_urgent_patient(urgent_patient: PatientCreate):
    """Urgent patient - patient without any documents,
    without known first_name, middle_name, last_name or any

    :param urgent_patient:
    :return:
    """
    if urgent_patient.without_documents:
        patient_uuid = uuid.uuid4().__str__()
        urgent_patient.first_name = patient_uuid
        urgent_patient.last_name = patient_uuid
    return urgent_patient


class CRUDPatient(CRUDBase[Patients, PatientCreate, PatientUpdate]):
    def create_patient(self, db: Session, *, obj_in: PatientCreate) -> Patients:
        obj_in = create_urgent_patient(obj_in)
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


patient = CRUDPatient(Patients)
