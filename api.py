import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
model = joblib.load("deployment/best_lgbm_hybrid_model.pkl")

class PatientData(BaseModel):
    HighBP: float; HighChol: float; CholCheck: float; BMI: float; Smoker: float
    Stroke: float; HeartDiseaseorAttack: float; PhysActivity: float; Fruits: float
    Veggies: float; HvyAlcoholConsump: float; AnyHealthcare: float; NoDocbcCost: float
    GenHlth: float; MentHlth: float; PhysHlth: float; DiffWalk: float; Sex: float
    Age: float; Education: float; Income: float

@app.post("/predict")
def predict_risk(data: PatientData):
    # Kỹ nghệ đặc trưng
    bmi_risk = 1.0 if data.BMI >= 25 else 0.0
    metabolic = data.HighBP + data.HighChol + bmi_risk
    lifestyle = data.Smoker + data.HvyAlcoholConsump
    decline = data.GenHlth + (data.PhysHlth / 30.0)
    
    input_df = pd.DataFrame([{
        **data.dict(),
        'Metabolic_Score': metabolic,
        'Lifestyle_Risk': lifestyle,
        'Health_Decline': decline
    }])
    
    prob = model.predict_proba(input_df)[0][1]
    prediction = 1 if prob >= 0.30 else 0
    
    return {
        "risk_probability": round(prob * 100, 2),
        "result_code": prediction,
        "recommendation": "Cần can thiệp y tế sớm" if prediction == 1 else "Duy trì lối sống hiện tại"
    }