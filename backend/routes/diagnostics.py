from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, delete
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, Response

from lib.diagnostics_models import NewDiagnostic
from utils.crud import get_session
from utils.db_init import Diagnostics

diagnostics_router = APIRouter()


@diagnostics_router.get("/")
async def get_diagnostics(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    diagnostics = session.query(Diagnostics).offset(offset).limit(limit).all()
    result = [
        {
            "id": diagnostic.id,
            "name": diagnostic.name,
            "expired_in_months": diagnostic.expired_in_months,
        }
        for diagnostic in diagnostics
    ]
    return JSONResponse(result)


@diagnostics_router.get("/{diagnostic_id}")
async def get_diagnostics(diagnostic_id: int, session: Session = Depends(get_session)):
    diagnostic = (
        session.query(Diagnostics).filter(Diagnostics.id == diagnostic_id).first()
    )
    if diagnostic is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(
        {
            "id": diagnostic.id,
            "name": diagnostic.name,
            "expired_in_months": diagnostic.expired_in_months,
        }
    )


@diagnostics_router.put("/")
async def add_diagnostics(
    diagnostic_data: NewDiagnostic, session: Session = Depends(get_session)
):
    stmt = insert(Diagnostics).values(**diagnostic_data.dict())
    session.execute(stmt)
    return Response(status_code=200)


@diagnostics_router.delete("/{diagnostic_id}")
async def delete_diagnostics(
    diagnostic_id: int, session: Session = Depends(get_session)
):
    stmt = delete(Diagnostics).where(Diagnostics.id == diagnostic_id)
    session.execute(stmt)
    return Response(status_code=200)
