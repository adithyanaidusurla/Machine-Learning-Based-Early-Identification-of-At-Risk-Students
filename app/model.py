import joblib

MODEL_PATH = "artifacts/student_risk_model.joblib"

def load_model():
    return joblib.load(MODEL_PATH)