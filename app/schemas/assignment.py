from pydantic import BaseModel


class AssignmentResponse(BaseModel):
    message: str
    doctor_id: int
    patient_id: int