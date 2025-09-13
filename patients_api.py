from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', example='P001')]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient belongs to')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the pateint in M')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in KGs')]
    
    @computed_field()
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    def verdict(self) -> str:
        
        if self.bmi < 18.5:
         return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'



def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


@app.get('/')
def hello():
    return {'Message': 'Patient Management System API'}

@app.get('/about')
def about():
    return {'Message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()

    return data


#TO VIEW THE DATA OF SPECIFIC PETIENT
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the Patient in the Database', example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient Not Found')

#TO VIEW THE DATA IN SPECIFIC Order
@app.get('/sort')
def sort_patient(sort_by: str = Query(..., description='Sort on the basis of height and weight'), order: str = Query('asc', description='sort in asc or dsc order')):

    valid_fields = ['height', 'weight']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid fields select from {valid_fields}')
    
    if order not in ['asc', 'dsc']:
        raise HTTPException(status_code=400, detail='Invalid Order: Select between asc ov dsc')
    
    data = load_data()

    sort_order = True if order=='dsc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    #Load Existing Data
    data = load_data()

    #Check if the patient data exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exist')

    #New patient will be added in the data base
    data[patient.id] = patient.model_dump(exclude=['id'])

    #saving the data in json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created succssfully'})



