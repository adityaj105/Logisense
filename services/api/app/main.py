from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PredictRequest(BaseModel):
    features: dict

@app.post('/predict')
def predict(req: PredictRequest):
    return {"prediction": None}
