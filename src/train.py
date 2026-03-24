import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import os

# 1. Load Processed Data
def load_data(file_path):
    df = pd.read_csv(file_path)

    # 1. Drop any rows that still have NaN (safety first)
    df = df.dropna()
    # 2. Drop any columns that are entirely empty (like 'subtype' if it stayed)
    df = df.dropna(axis=1, how='all')
    # ---------------------------

    
    # 2. DROP LEAKAGE AND NON-NUMERIC COLUMNS
    # 'price_by_m2' is the "cheat" column. 
    # 'furnished' is causing the string error.
    # 'building_state' might have NaNs (empty values).
    cols_to_drop = ['price_by_m2', 'furnished', 'building_state']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

    # 3. FILL OR DROP MISSING VALUES
    # For numeric columns like 'build_year' or 'land_area_m2', fill with 0 or median
    df = df.fillna(0) 

    # 4. FINAL TYPE CHECK (Force everything to float)
    # This solves the "KeyError: 'object'" for XGBoost
    X = df.drop(columns=['price'])
    X = X.astype(float) 
    y = df['price']
   
    return train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Evaluation Function
def evaluate_model(name, model, X_test, y_test):
    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Model: {name}")
    print(f"  - R² Score: {r2:.4f}")
    print(f"  - MAE: {mae:.2f} €")
    return r2

if __name__ == "__main__":
    DATA_PATH = 'data/clean_data_for_model.csv' # or processed_rent_data.csv
    
    if not os.path.exists(DATA_PATH):
        print("Error: Cleaned data file not found. Run preprocessing.py first!")
    else:
        X_train, X_test, y_train, y_test = load_data(DATA_PATH)
        
        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
            "XGBoost": XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=8, sample_rate=0.8, colsample_bytree=0.8, random_state=42)
        }
        
        best_model = None
        best_score = -np.inf
        best_name = ""

        print("--- Training Models ---")
        for name, model in models.items():
            model.fit(X_train, y_train)
            score = evaluate_model(name, model, X_test, y_test)
            
            if score > best_score:
                best_score = score
                best_model = model
                best_name = name

        # 3. Save the Best Model
        os.makedirs('models', exist_ok=True)
        model_filename = 'models/best_model.pkl'
        joblib.dump(best_model, model_filename)
        
        # Save the column names (needed for the dashboard to match the input)
        joblib.dump(X_train.columns.tolist(), 'models/model_columns.pkl')
        
        print(f"\n🏆 Best Model: {best_name} with R²: {best_score:.4f}")
        print(f"✅ Saved to {model_filename}")