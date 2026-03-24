import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'best_model.pkl')
COLUMNS_PATH = os.path.join(BASE_DIR, 'models', 'model_columns.pkl')

# Load model and columns
model = joblib.load(MODEL_PATH)
model_columns = joblib.load(COLUMNS_PATH)

st.set_page_config(page_title="Immo-Eliza Price Predictor", layout="centered")

st.title("🏠 Immo-Eliza: Belgium Real Estate Predictor")
st.markdown("Enter property details below to estimate the **Market Sale Price**.")

# --- 2. INPUT FORM ---
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        zip_code = st.number_input("Zip Code", min_value=1000, max_value=9999, value=1000)
        living_area = st.number_input("Living Area (m²)", min_value=10, max_value=1000, value=150)
        rooms = st.slider("Number of Bedrooms", 1, 10, 3)
        facades = st.slider("Number of Facades", 1, 4, 2)
        
    with col2:
        land_area = st.number_input("Land Area (m²)", min_value=0, max_value=10000, value=500)
        # ADDED: Actual Price input for comparison
        actual_price = st.number_input("Actual Asking Price (€)", min_value=0, step=5000, value=0, help="Enter the price listed on the website to compare with AI")
        build_year = st.number_input("Build Year", min_value=1800, max_value=2024, value=2000)
        
        # Checkboxes grouped
        st.write("**Amenities**")
        has_garden = st.checkbox("Garden")
        has_terrace = st.checkbox("Terrace")
        has_swimming_pool = st.checkbox("Swimming Pool")

    prop_type = st.selectbox("Property Type", ["House", "Flat", "Villa", "Penthouse"])
    submit = st.form_submit_button("Estimate Price")

# --- 3. PREDICTION LOGIC ---
if submit:
    # Prepare input DataFrame
    input_data = pd.DataFrame(0, index=[0], columns=model_columns)
    
    # Mapping logic (covers common naming variations from your training)
    mapping = {
        'zip_code': zip_code, 'zipcode': zip_code,
        'livable_surface_m2': living_area, 'living_area': living_area,
        'number_of_bedrooms': rooms, 'nb_rooms': rooms,
        'land_area_m2': land_area, 'surface_land': land_area,
        'number_of_facades': facades, 'facades': facades,
        'build_year': build_year,
        'has_garden': int(has_garden),
        'has_terrace': int(has_terrace),
        'has_swimming_pool': int(has_swimming_pool)
    }
    
    for key, value in mapping.items():
        if key in input_data.columns:
            input_data[key] = value

    # Handle One-Hot Encoding for Property Type
    type_col = f"prop_group_{prop_type.lower()}"
    if type_col in input_data.columns:
        input_data[type_col] = 1

    # Execute Prediction
    prediction = float(model.predict(input_data)[0])
    
    # --- 4. DISPLAY RESULTS ---
    st.markdown("---")
    st.subheader("Price Analysis Results")
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.metric(label="🤖 AI Estimated Price", value=f"€{prediction:,.0f}")
        
    with res_col2:
        if actual_price > 0:
            diff = actual_price - prediction
            percent_diff = (diff / prediction) * 100
            # Delta color is 'inverse' so that if Actual > Predicted (Positive), it shows as Red (Expensive)
            st.metric(label="🏠 Actual Asking Price", 
                      value=f"€{actual_price:,.0f}", 
                      delta=f"{percent_diff:.1f}% vs AI", 
                      delta_color="inverse")
        else:
            st.info("Enter an 'Actual Price' in the form to see the comparison delta.")

    # Final Verdict Message
    if actual_price > 0:
        if actual_price > prediction * 1.15:
            st.error("🚨 **Verdict:** This property seems **Overpriced** compared to market trends.")
        elif actual_price < prediction * 0.85:
            st.success("💎 **Verdict:** This property appears to be a **Good Deal**!")
        else:
            st.info("⚖️ **Verdict:** The asking price is **Fair** and matches AI expectations.")
    else:
        st.success(f"### 💰 Estimated Value: €{prediction:,.2f}")

    st.caption("Prediction based on XGBoost analysis of Immovlan.be market data.")




    st.info("This prediction is based on XGBoost analysis of 10,100 listings.")
