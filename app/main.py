from fastapi import FastAPI
import pandas as pd

from app.model import load_model
from app.schemas import StudentInput

app = FastAPI(
    title="Machine Learning Based Early Identification of At Risk Students",
    description="Predicts if a student is at academic risk",
    version="1.0"
)

model = load_model()

@app.get("/")
def health_check():
    return {"status": "API is running"}

@app.post("/predict")
def predict_risk(student: StudentInput):

    data = pd.DataFrame([student.model_dump()])

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    return {
        "at_risk": bool(prediction),
        "risk_probability": round(float(probability), 3)
    }