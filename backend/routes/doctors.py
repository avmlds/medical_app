from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, Response

from lib.doctors_models import NewDoctor
from utils.crud import get_session
from utils.db_init import Doctors

doctors_router = APIRouter()


@doctors_router.get("/")
async def get_doctors(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    doctors = session.query(Doctors).offset(offset).limit(limit).all()
    result = [
        {
            "id": doctor.id,
            "name": doctor.name,
            "expires_in_days": doctor.expires_in_days,
        }
        for doctor in doctors
    ]
    return JSONResponse(result)


@doctors_router.get("/{doctor_id}")
async def get_doctor(doctor_id: int, session: Session = Depends(get_session)):
    doctor = session.query(Doctors).filter(Doctors.id == doctor_id).first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(
        {
            "id": doctor.id,
            "name": doctor.name,
            "expires_in_days": doctor.expires_in_days,
        }
    )


@doctors_router.put("/")
async def add_doctor(doctor_data: NewDoctor, session: Session = Depends(get_session)):
    stmt = (
        insert(Doctors)
        .values(**doctor_data.dict())
        .on_conflict_do_update(
            constraint="doctors_name_key", set_={"name": doctor_data.name}
        )
        .returning(Doctors.id)
    )
    result = session.execute(stmt)
    data = result.first()["id"]
    return JSONResponse(content={"id": data}, status_code=200)


@doctors_router.delete("/{doctor_id}")
async def delete_doctor(doctor_id: int, session: Session = Depends(get_session)):
    stmt = delete(Doctors).where(Doctors.id == doctor_id)
    session.execute(stmt)
    return Response(status_code=200)
