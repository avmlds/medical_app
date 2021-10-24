from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from starlette.responses import Response, JSONResponse

from lib.patient_models import NewPatient, LinkDiagnostics, LinkDoctors
from utils.crud import get_session
from utils.db_init import (
    Patients,
    PatientDoctors,
    PatientDiagnostics,
    Diagnostics,
    Doctors,
)

patient_router = APIRouter()


@patient_router.get("/")
async def get_patients(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    patients = session.query(Patients).offset(offset).limit(limit).all()
    result = [
        {
            "id": patient.id,
            "first_name": patient.first_name,
            "middle_name": patient.middle_name,
            "last_name": patient.last_name,
            "birth_date": patient.birth_date.isoformat(),
            "to_committee": patient.to_committee,
            "to_internat": patient.to_internat,
        }
        for patient in patients
    ]
    return JSONResponse(result)


@patient_router.get("/{patient_id}")
async def get_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.query(Patients).filter(Patients.id == patient_id).first()
    doctors = (
        session.query(PatientDoctors.last_at, Doctors.name)
        .join(Doctors, PatientDoctors.doctor_id == Doctors.id)
        .order_by(PatientDoctors.last_at.desc())
        .filter(PatientDoctors.patient_id == patient_id)
    ).all()
    diagnostics = (
        session.query(Diagnostics.name, PatientDiagnostics.last_at)
        .join(Diagnostics, PatientDiagnostics.diagnostic_id == Diagnostics.id)
        .order_by(PatientDiagnostics.last_at.desc())
        .filter(PatientDiagnostics.patient_id == patient_id)
    ).all()

    patient_doctors = []
    if len(doctors) > 0:
        patient_doctors = [
            {"name": doctor[0], "last_at": doctor[1].isoformat()} for doctor in doctors
        ]

    patient_diagnostics = []
    if len(diagnostics) > 0:
        patient_diagnostics = [
            {"name": diagnostic[0], "last_at": diagnostic[1].isoformat()}
            for diagnostic in diagnostics
        ]

    if patient is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(
        {
            "id": patient.id,
            "first_name": patient.first_name,
            "middle_name": patient.middle_name,
            "last_name": patient.last_name,
            "birth_date": patient.birth_date.isoformat(),
            "to_committee": patient.to_committee,
            "to_internat": patient.to_internat,
            "doctors": patient_doctors,
            "diagnostics": patient_diagnostics,
        }
    )


@patient_router.put("/")
async def add_patient(
    patient_data: NewPatient, session: Session = Depends(get_session)
):
    stmt = insert(Patients).values(**patient_data.dict())
    session.execute(stmt)
    return Response(status_code=200)


@patient_router.delete("/{patient_id}")
async def delete_patient(patient_id: int, session: Session = Depends(get_session)):
    stmt = delete(Patients).where(Patients.id == patient_id)
    session.execute(stmt)
    return Response(status_code=200)


@patient_router.get("/{patient_id}/diagnostics")
async def get_patient_diagnostics(
    patient_id: int,
    expired_in: Optional[int] = None,
    session: Session = Depends(get_session),
):
    results = (
        session.query(Patients, Diagnostics)
        .join(PatientDiagnostics, Patients.id == PatientDiagnostics.patient_id)
        .join(Diagnostics, PatientDiagnostics.diagnostic_id == Diagnostics.id)
        .filter(Patients.id == patient_id)
        .all()
    )
    if results is None or len(results[0]) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    patient = results[0][0]
    data = [
        {
            "id": patient.id,
            "first_name": patient.first_name,
            "middle_name": patient.middle_name,
            "last_name": patient.last_name,
            "birth_date": patient.birth_date.isoformat(),
            "to_committee": patient.to_committee,
            "to_internat": patient.to_internat,
            "diagnostic": [
                {
                    "diagnostic": result[1].name,
                    "expired_id": result[1].expired_in_months,
                }
                for result in results
            ],
        }
        for patient_result in results
    ]
    return JSONResponse(data)


@patient_router.get("/{patient_id}/doctors")
async def get_patient_doctors(
    patient_id: int,
    expired_in: Optional[int] = None,
    session: Session = Depends(get_session),
):
    results = (
        session.query(Patients, Doctors)
        .join(PatientDoctors, Patients.id == PatientDoctors.patient_id)
        .join(Doctors, PatientDoctors.doctor_id == Doctors.id)
        .filter(Patients.id == patient_id)
        .all()
    )
    if results is None or len(results[0]) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    patient = results[0][0]
    data = {
        "id": patient.id,
        "first_name": patient.first_name,
        "middle_name": patient.middle_name,
        "last_name": patient.last_name,
        "birth_date": patient.birth_date.isoformat(),
        "to_committee": patient.to_committee,
        "to_internat": patient.to_internat,
        "doctors": [
            {"doctor": result[1].name, "expired_id": result[1].expired_in_months}
            for result in results
        ],
    }
    return JSONResponse(data)


@patient_router.post("/{patient_id}/diagnostics/{diagnostic_id}")
async def link_patient_diagnostics(
    patient_id: int,
    diagnostic_id: int,
    data: LinkDiagnostics,
    session: Session = Depends(get_session),
):
    stmt = insert(PatientDiagnostics).values(
        patient_id=patient_id, diagnostic_id=diagnostic_id, last_at=data.last_at
    )
    session.execute(stmt)
    return Response(status_code=200)


@patient_router.post("/{patient_id}/doctors/{doctor_id}")
async def link_patient_doctors(
    patient_id: int,
    doctor_id: int,
    data: LinkDoctors,
    session: Session = Depends(get_session),
):
    stmt = insert(PatientDoctors).values(
        patient_id=patient_id, doctor_id=doctor_id, last_at=data.last_at
    )
    session.execute(stmt)
    return Response(status_code=200)


@patient_router.delete("/{patient_id}/diagnostics/{diagnostic_id}")
async def delete_link_patient_diagnostics(
    patient_id: int,
    diagnostic_id: int,
    session: Session = Depends(get_session),
):
    stmt = delete(PatientDiagnostics).where(
        patient_id=patient_id, diagnostic_id=diagnostic_id
    )
    session.execute(stmt)
    return Response(status_code=200)


@patient_router.delete("/{patient_id}/doctors/{doctor_id}")
async def delete_link_patient_doctors(
    patient_id: int,
    doctor_id: int,
    session: Session = Depends(get_session),
):
    stmt = delete(PatientDoctors).where(patient_id=patient_id, doctor_id=doctor_id)
    session.execute(stmt)
    return Response(status_code=200)
