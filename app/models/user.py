from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="doctor")
    is_active = Column(Boolean, default=True)

    doctor_id = Column(Integer,ForeignKey("doctors.id"),nullable=True)