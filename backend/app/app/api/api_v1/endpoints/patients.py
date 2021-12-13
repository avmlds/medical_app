from typing import List, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Patient])
def read_patients(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    return crud.patient.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Patient)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.PatientCreate,
) -> Any:
    """
    Create new patient.
    """
    item = crud.patient.create_patient(db=db, obj_in=item_in)
    return item
