from pydantic import (
    BaseModel,
    EmailStr,
    AnyUrl,
    Field,
    field_validator,
)  # data validation
from typing import List, Dict, Optional, Annotated  # type validation


class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=50,
            title="name of the patient",
            description="give the name of the patient in less than 50 chars",
            examples=["shihab", "Rakib"],
        ),
    ]

    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Optional[bool] = None  # can make a variable optional
    allergies: Optional[List[str]] = Field(max_length=5)
    contact_details: Dict[str, str]

    # Field validation
    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domain = ["hdfc.com", "icici.com"]
        domain_name = value.split("@")[-1]
        if domain_name not in valid_domain:
            raise ValueError("Not a valid domain")
        return value


def insert_patient_data(p: Patient):
    print(p.name)
    print(p.age)
    print("inserted into database")


def update_patient_data(p: Patient):
    print(p.name)
    print(p.age)
    print("Update into database")


patient_info = {
    "name": "shihab",
    "email": "a@hdfc.com",
    "linkedin_url": "http://linkedin.com/sdk",
    "age": 30,
    "weight": 75.2,
    "married": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {"phone": "01w398478"},
}


patient1 = Patient(**patient_info)

insert_patient_data(patient1)
