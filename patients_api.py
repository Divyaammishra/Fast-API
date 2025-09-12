from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data


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

#Continue late