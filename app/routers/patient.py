from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user

from app.database import get_db

from app.models.doc_pat import DoctorPatient
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import (PatientCreate,PatientResponse,PatientUpdate)

router = APIRouter(prefix="/patients",tags=["Patients"])

@router.post("",response_model=PatientResponse,status_code=status.HTTP_201_CREATED)
def create_patient(patient_data: PatientCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    patient = Patient(
        name=patient_data.name,
        age=patient_data.age,
        phone=patient_data.phone)

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


@router.get( "",response_model=list[PatientResponse])
def get_patients(page: int = Query(default=1, ge=1),limit: int = Query(default=10, ge=1, le=100),db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if current_user.role == "admin":

        query = db.query(Patient)

    elif current_user.role == "doctor":

        query = (db.query(Patient).join(DoctorPatient,Patient.id == DoctorPatient.patient_id)
            .filter(DoctorPatient.doctor_id ==current_user.doctor_id))

    else:
        raise HTTPException(status_code=403,detail="Access denied")

    offset = (page - 1) * limit

    patients = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return patients


@router.get("/{patient_id}",response_model=PatientResponse)
def get_patient(patient_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404,detail="Patient not found")

    if current_user.role == "doctor":

        assignment = db.query(DoctorPatient).filter(DoctorPatient.doctor_id == current_user.doctor_id,DoctorPatient.patient_id == patient_id).first()

        if not assignment:
            raise HTTPException(status_code=403,detail="You can only view your assigned patients")

    elif current_user.role != "admin":

        raise HTTPException(status_code=403,detail="Access denied")

    return patient

@router.put("/{patient_id}",response_model=PatientResponse)
def update_patient(patient_id: int,patient_data: PatientUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    patient = db.query(Patient).filter( Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404,detail="Patient not found")

    if patient_data.name is not None:
        patient.name = patient_data.name

    if patient_data.age is not None:
        patient.age = patient_data.age

    if patient_data.phone is not None:
        patient.phone = patient_data.phone

    db.commit()
    db.refresh(patient)

    return patient


@router.delete("/{patient_id}")
def delete_patient(patient_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Admin access required")

    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404,detail="Patient not found")

    db.delete(patient)
    db.commit()

    return {"message": "Patient deleted successfully"}