from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
from pathlib import Path as FilePath
import json

app = FastAPI()
DATA_FILE = FilePath(__file__).with_name("patient.json")

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name:Annotated[str,Field(...,description="Name of the patient")]
    age: Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    height:Annotated[float,Field(...,gt=0,description="Height of the patient meters")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the patient in kgs")]
    gender: Annotated[
        Literal['male', 'female', 'others'],
        Field(..., description='Gender of the patient'),
    ]
    blood_group:str
    diagnosis:str
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/self.height**2)
        return bmi
    
    
def load_data():
    with DATA_FILE.open("r") as f:
        data = json.load(f)
    return data
def save_data(data):
    with DATA_FILE.open('w') as f:
        json.dump(data,f)

@app.get("/")
def home():
    return {"message": "Patient Management system"}


@app.get("/about")
def about():
    return {"message": "Fully functional API to manage your patient records"}


@app.get("/contact")
def contact():
    return {"email": "example@gmail.com"}


# @app.get("/shihab/{name}")
# def shihab(name:str):
#     return {"name":"MD Ashadujjaman shihab",
#             "id":"2311104",
#             "subject":"CSE",
#             "qote":"Fuck you"
#             }
@app.get("/view")
def view():
    data = load_data()
    return data


@app.get("/patient/{patientId}")
def view_patient(
    patientId: str = Path(
        ..., description="ID of the patient in the DB", examples=["P001"]
    )
):
    data = load_data()
    if patientId in data:
        return data[patientId]
    # return {'error':'Patient not found'}
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patient(
    sort_by: str = Query(..., description="sort on the basis of age"),
    order: str = Query("asc", description="sort in asc or desc order"),
):
    valid_fields = ["age"]
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"invalid field; select from {valid_fields}",
        )
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400, detail="invalid order select between asc or desc"
        )
    data = load_data()

    sort_order = True if order == "desc" else False
    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order
    )
    return sorted_data


@app.post('/create')
def create_patient(patient:Patient):
    #laod existing data
    data=load_data()
    
    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='patient already exists')
    
    #new patient add to the database
    data[patient.id]= patient.model_dump(exclude=['id'])
    
    #save into the json file
    save_data(data)
    return JSONResponse(status_code=201, content='Patient created successfully')
    
    
    
