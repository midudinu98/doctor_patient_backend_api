from fastapi import FastAPI

from app.database import Base,engine
from app.models import User,Doctor,Patient,DoctorPatient

from app.routers.auth import router as auth_router
from app.routers.doctor import router as doctors_router
from app.routers.patient import router as patient_router
from app.routers.assignment import router as assignment_router

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Doctor Patient API Management")

app.include_router(auth_router)
app.include_router(doctors_router)
app.include_router(patient_router)
app.include_router(assignment_router)


@app.get("/")
def root():
    return{"message":"API is Running"}

