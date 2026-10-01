from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import (get_current_user,require_admin)

from app.database import get_db

from app.models.doctor import Doctor
from app.models.user import User

from app.schemas.doctor import (DoctorCreate,DoctorResponse,DoctorUpdate)

router = APIRouter(prefix="/doctors",tags=["Doctors"])

@router.post("",response_model=DoctorResponse,status_code=status.HTTP_201_CREATED)
def create_doctor(doctor_data: DoctorCreate,db: Session = Depends(get_db),current_user: User = Depends(require_admin)):
    existing_doctor = db.query(Doctor).filter(Doctor.email == doctor_data.email).first()

    if existing_doctor:
        raise HTTPException(status_code=400,detail="Doctor email already exists")

    doctor = Doctor(
        name=doctor_data.name,
        specialization=doctor_data.specialization,
        email=doctor_data.email,
        is_active=True)

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor


@router.get("",response_model=list[DoctorResponse])
def get_doctors(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
   
    offset = (page - 1) * limit

    doctors = (
        db.query(Doctor)
        .filter(Doctor.is_active == True)
        .offset(offset)
        .limit(limit)
        .all())

    return doctors

@router.get("/{doctor_id}",response_model=DoctorResponse)
def get_doctor(doctor_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id,Doctor.is_active == True).first()

    if not doctor:
        raise HTTPException(status_code=404,detail="Doctor not found")

    return doctor


@router.put("/{doctor_id}",response_model=DoctorResponse)
def update_doctor(doctor_id: int,doctor_data: DoctorUpdate,db: Session = Depends(get_db),current_user: User = Depends(require_admin)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404,detail="Doctor not found")

    if not doctor.is_active:
        raise HTTPException(status_code=400,detail="Doctor is inactive")

    if doctor_data.name is not None:
        doctor.name = doctor_data.name

    if doctor_data.specialization is not None:
        doctor.specialization = doctor_data.specialization

    if doctor_data.email is not None:

        existing_doctor = db.query(Doctor).filter(Doctor.email == doctor_data.email,Doctor.id != doctor_id).first()

        if existing_doctor:
            raise HTTPException(status_code=400,detail="Doctor email already exists")

        doctor.email = doctor_data.email

    db.commit()
    db.refresh(doctor)

    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int,db: Session = Depends(get_db),current_user: User = Depends(require_admin)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404,detail="Doctor not found")

    if not doctor.is_active:
        raise HTTPException(status_code=400,detail="Doctor is already inactive")

    doctor.is_active = False

    db.commit()

    return {"message": "Doctor deactivated successfully"}