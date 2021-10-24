import uvicorn
from fastapi import FastAPI

from routes.doctors import doctors_router
from routes.patients import patient_router
from routes.diagnostics import diagnostics_router

app = FastAPI()

app.include_router(doctors_router, prefix="/doctors", tags=["doctors"])
app.include_router(patient_router, prefix="/patients", tags=["patients"])
app.include_router(diagnostics_router, prefix="/diagnostics", tags=["diagnostics"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
