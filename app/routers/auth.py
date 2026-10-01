from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.doctor import Doctor

from app.auth.security import (create_access_token,hash_password,verify_password)

from app.database import get_db

from app.models.user import User

from app.schemas.auth import (LoginRequest,RegisterRequest,TokenResponse)


router = APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/register",status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")

    if request.role not in ["admin", "doctor"]:
        raise HTTPException(status_code=400,detail="Role must be admin or doctor")

    if request.role == "doctor":
        if request.doctor_id is None:
            raise HTTPException(status_code=400,detail="doctor_id is required for doctor")

        doctor = db.query(Doctor).filter(Doctor.id == request.doctor_id).first()

        if not doctor:
            raise HTTPException(status_code=404,detail="Doctor not found")

    if request.role == "admin":
        if request.doctor_id is not None:
            raise HTTPException(status_code=400,detail="Admin cannot have doctor_id")

    hashed_password = hash_password( request.password)

    user = User(
        username=request.username,
        email=request.email,
        password_hash=hashed_password,
        role=request.role,
        doctor_id=request.doctor_id)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "doctor_id": user.doctor_id}


@router.post("/login",response_model=TokenResponse)
def login(request: LoginRequest,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=401,detail="Invalid email or password")

    if not verify_password(request.password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403,detail="User account is inactive")

    access_token = create_access_token({"sub": str(user.id),"role": user.role})

    return {"access_token": access_token,"token_type": "bearer"}