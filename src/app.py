import os
import uvicorn
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Enable CORS for Lovable/Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model and Column structure
model = joblib.load("models/best_model.pkl")
model_columns = joblib.load("models/model_columns.pkl")

class HouseData(BaseModel):
    zip_code: int
    living_area: int
    rooms_number: int
    facades_number: int
    land_area: int
    actual_price: Optional[int] = 0
    build_year: int = 2000
    garden: bool = False
    terrace: bool = False
    swimming_pool: bool = False
    property_type: str = "House" # Added to match Streamlit's selectbox


@app.get("/")
def read_root():
    return {"status": "alive", "message": "Immo-Eliza API is running"}

@app.post("/predict")
def predict_price(data: HouseData):
    # 1. Initialize DataFrame with 0s using model columns
    input_df = pd.DataFrame(0, index=[0], columns=model_columns)
    
    # 2. EXACT Mapping logic from your Streamlit code
    mapping = {
        'zip_code': data.zip_code, 'zipcode': data.zip_code,
        'livable_surface_m2': data.living_area, 'living_area': data.living_area,
        'number_of_bedrooms': data.rooms_number, 'nb_rooms': data.rooms_number,
        'land_area_m2': data.land_area, 'surface_land': data.land_area,
        'number_of_facades': data.facades_number, 'facades': data.facades_number,
        'build_year': data.build_year,
        'has_garden': int(data.garden),
        'has_terrace': int(data.terrace),
        'has_swimming_pool': int(data.swimming_pool)
    }
    
    # Fill columns if they exist in the model
    for key, value in mapping.items():
        if key in input_df.columns:
            input_df[key] = value

    # 3. Handle Property Type One-Hot Encoding (Exactly like Streamlit)
    type_col = f"prop_group_{data.property_type.lower()}"
    if type_col in input_df.columns:
        input_df[type_col] = 1

    # 4. Execute Prediction
    prediction = float(model.predict(input_df)[0])
    
    # 5. Logic for Verdict
    difference = 0
    verdict = "N/A"
    if data.actual_price > 0:
        difference = data.actual_price - prediction
        if data.actual_price > prediction * 1.15:
            verdict = "Overpriced"
        elif data.actual_price < prediction * 0.85:
            verdict = "Good Deal"
        else:
            verdict = "Fair Price"

    return {
        "predicted_price": round(prediction, 2),
        "actual_price": data.actual_price,
        "difference": round(difference, 2),
        "verdict": verdict
    }



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)