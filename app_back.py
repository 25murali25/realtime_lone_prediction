from fastapi import FastAPI
import pickle
import pandas as pd
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class LoadData(BaseModel):
    Gender:str
    Married:str
    Dependents:str
    Education:str
    Self_Employed:str
    ApplicantIncome:float
    CoapplicantIncome:float
    LoanAmount:float
    Loan_Amount_Term:float
    Credit_History:float
    Property_Area:str

model = None    
@app.on_event('startup')
def load_data():
    global model 
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)  
    
@app.post('/lone_prediction')
def lone_prediction_status(data:LoadData):
    try:
        model_input = pd.DataFrame([data.dict()]) 
        prediction = model.predict(model_input)[0]
        if prediction == 1:
            return {'prediction': 'Loan Approved'}
        else:
            return {'prediction': 'Loan Rejected'}
    except Exception as e:
        return {'error':str(e)}  
    
if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0",port=8001)    
      
    
    