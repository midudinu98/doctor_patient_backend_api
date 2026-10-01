from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user

from app.database import get_db

from app.models.doctor import Doctor
from app.models.doc_pat import DoctorPatient
from app.models.patient import Patient
from app.models.user import User

from app.schemas.assignment import AssignmentResponse
from app.schemas.patient import PatientResponse


router = APIRouter(prefix="/doctors",tags=["Doctor Patients"])

@router.post("/{doctor_id}/patients/{patient_id}",response_model=AssignmentResponse,status_code=status.HTTP_201_CREATED)
def assign_patient(
    doctor_id: int,
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    # Only admin can assign patients
    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Admin access required")

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404,detail="Doctor not found")

    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404,detail="Patient not found")

    existing_assignment = db.query(DoctorPatient).filter(DoctorPatient.doctor_id == doctor_id,DoctorPatient.patient_id == patient_id).first()

    if existing_assignment:raise HTTPException(status_code=400,detail="Patient already assigned to this doctor")

    assignment = DoctorPatient(doctor_id=doctor_id,patient_id=patient_id)

    db.add(assignment)
    db.commit()

    return {
        "message": "Patient assigned successfully",
        "doctor_id": doctor_id,
        "patient_id": patient_id }

@router.get("/{doctor_id}/patients",response_model=list[PatientResponse])
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    if current_user.role == "doctor":

        if current_user.doctor_id != doctor_id:
            raise HTTPException(status_code=403,detail="You can only view your assigned patients")

    elif current_user.role != "admin":
            raise HTTPException(status_code=403,detail="Access denied")

    doctor = db.query(Doctor).filter( Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404,detail="Doctor not found")

    patients = db.query(Patient).join(DoctorPatient,Patient.id == DoctorPatient.patient_id)

    return patients