from pydantic import BaseModel, Field, field_validator


class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):
        if not value.isdigit():
            raise ValueError("Phone must contain only digits")

        if not 10 <= len(value) <= 15:
            raise ValueError(
                "Phone must contain 10 to 15 digits"
            )

        return value


class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = Field(default=None, gt=0)
    phone: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value

        if not value.isdigit():
            raise ValueError("Phone must contain only digits")

        if not 10 <= len(value) <= 15:
            raise ValueError(
                "Phone must contain 10 to 15 digits"
            )

        return value


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str

    class Config:
        from_attributes = True