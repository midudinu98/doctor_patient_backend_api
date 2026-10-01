from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base

class Doctor(Base):
    
    __tablename__= "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True)