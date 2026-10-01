from sqlalchemy import Column, ForeignKey, Integer
from app.database import Base

class DoctorPatient(Base):
   
    __tablename__ = "doctor_patient"

    doctor_id = Column(Integer,ForeignKey("doctors.id"),primary_key=True)
    patient_id = Column(Integer,ForeignKey("patients.id"),primary_key=True)