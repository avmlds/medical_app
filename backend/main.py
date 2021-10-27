import uvicorn
from fastapi import FastAPI

from routes.doctors import doctors_router
from routes.patients import patient_router
from routes.diagnostics import diagnostics_router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
        allow_headers=["*"],
    ),
]

app = FastAPI(middleware=middleware)

app.include_router(doctors_router, prefix="/doctors", tags=["doctors"])
app.include_router(patient_router, prefix="/patients", tags=["patients"])
app.include_router(diagnostics_router, prefix="/diagnostics", tags=["diagnostics"])
