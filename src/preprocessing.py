import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from utils import get_province

# --- 1. CLEANING FUNCTIONS ---

def clean_immo_data(df):
    # 1. Clean the 'type_of_sale' column
    df['type_of_sale'] = df['type_of_sale'].str.lower().str.strip()
    # If the URL contains 'rent', it's a rental. Otherwise, it's likely a sale.
    df.loc[df['url'].str.contains('rent', case=False), 'type_of_sale'] = 'rent'
    df['type_of_sale'] = df['type_of_sale'].replace('for', 'rent') # Backup fix

    # Removing duplicates based on 'url' (assuming each property has a unique URL) and resetting index
    df = df.drop_duplicates(subset=['url']).reset_index(drop=True)
    
    # This regex looks for 4 digits (\d{4}) that are between two forward slashes
    df['postcode'] = df['url'].str.extract(r'/(\d{4})/')[0]

    # Convert to numeric to handle them easily later
    df['postcode'] = pd.to_numeric(df['postcode'], errors='coerce')
    df['province'] = df['postcode'].apply(get_province)

    
    # 2. Basic Cleaning
    # Remove rows where price is missing (our target variable) and reset index
    df = df.dropna(subset=['price']).reset_index(drop=True)
    
    # Drop rows missing target variables like 'living_area' and reset index
    df = df.dropna(subset=['price', 'living_area']).reset_index(drop=True)

    df = df[df['nb_rooms'] <= 10] # Removes extreme outliers like the 35-room property

    # --- 3. CLEANING ---
    # Drop variables with too much missing data (>50%) as per project
    cols_to_drop = ['open_fire', 'kitchen_equipped'] 
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    # Convert numeric columns (Scrapy sometimes saves them as strings)
    numeric_cols = ['price', 'nb_rooms', 'living_area', 'terrace_area', 
                    'garden_area', 'surface_land', 'plot_surface', 'facades']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 3. Feature Engineering
    # Create 'has_garden' and 'has_terrace' boolean features
    df['has_garden'] = df['garden_area'].apply(lambda x: 1 if x > 0 else 0)
    df['has_terrace'] = df['terrace_area'].apply(lambda x: 1 if x > 0 else 0)
    
    # 4. Outlier Removal (Critical for Real Estate)
    df = df[(df['price'] >= 100) & (df['price'] <= 5000000)]

    # Remove properties with 0 living area
    df = df[df['living_area'] > 10]

    # --- 5. STANDARDIZATION ---
    df['price_m2'] = df['price'] / df['living_area']
    df = df[df['price_m2'] <= 20000] # Remove abnormal price/m2

    return df

# --- 2. STATISTICAL OUTLIER REMOVAL FUNCTIONS ---

def remove_outliers_iqr(df, column):
    # Calculate quartiles and IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define bounds (standard 1.5 rule)
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filter the dataframe
    df_clean = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    print(f"Bounds: {lower_bound:.2f} to {upper_bound:.2f}")
    print(f"Removed {len(df) - len(df_clean)} outliers.")
    
    return df_clean

# EDA Function
def run_eda(df, label):
    print(f"\n--- EDA for {label} Properties ---")
    print(df.describe())
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nUnique Values:")
    for col in df.select_dtypes(include='object').columns:
        print(f"{col}: {df[col].nunique()} unique values")
    
    # Price Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], bins=50, kde=True, color='blue')
    plt.title(f'Price Distribution: {label} Properties')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.show()

    # Correlation Heatmap (Numeric Only)
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'Correlation Matrix ( {label} Features)')
    plt.show()
    
    # {label} Price by Province
    plt.figure(figsize=(10, 6))
    order = df.groupby('province')['price'].median().sort_values(ascending=False).index
    sns.boxplot(df, x='province', y='price', order=order)
    plt.title(f'{label} Price by Province')
    plt.show()

    
    #Correlation heatmap(Price vs Features)
    plt.figure(figsize=(12, 8))
    numeric_df = df.select_dtypes(include=[np.number])
    correlation_matrix = numeric_df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title(f'Correlation Heatmap for {label} Properties')
    plt.show()

    # Pairplot to visualize relationships between price and key features for {label} properties
    plt.figure(figsize=(12, 8))
    # Only correlate numeric columns
    sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'Correlation Matrix of Housing for {label} Features')
    plt.show()
    
    #Price by locality(Top 10 most expensive localities
    top_localities = df.groupby('locality')['price'].median().sort_values(ascending=False).head(10)
    top_localities.plot(kind='bar',figsize=(10, 6), color='orange')
    plt.title(f'Top 10 Most Expensive Localities (Median Price) for {label}')
    plt.xlabel('Locality')
    plt.ylabel('Average Price')         
    plt.xticks(rotation=45)
    plt.show()

    #Price by property type (House, Apartment, etc.)
    plt.figure(figsize=(10, 6)) 
    sns.boxplot(data=df, x='property_type', y='price', palette='Set2')
    plt.title(f'Price Distribution by Property Type for {label} Properties') 
    plt.xlabel('Property Type')
    plt.ylabel('Price (€)')
    plt.xticks(rotation=45)
    plt.show()

    #Average Price per m² by Province for rental properties
    plt.figure(figsize=(10, 6)) 
    order = df.groupby('province')['price_m2'].median().sort_values(ascending=False).index
    sns.barplot(data=df, x='province', y='price_m2', palette='viridis', order=order, estimator=np.median)
    plt.title(f'Average Price per m² by Province - {label} Properties')
    plt.ylabel('Median Price per m² (€)')
    plt.show()

    # Filter for Brussels region for sale properties
    brussels_df = df[df['province'] == 'Brussels']

    # Get Top 5 most expensive municipalities by Average Price
    top_5_brussels = brussels_df.groupby('locality')['price'].mean().sort_values(ascending=False).head(5)

    plt.figure(figsize=(10, 5))
    top_5_brussels.plot(kind='barh', color='#4c5678')
    plt.title(f'Most Expensive Municipalities for {label} properties — Brussels')
    plt.xlabel('Average Price (€)')
    plt.gca().invert_yaxis() # Highest on top
    plt.show()

    print(f"--- EDA Complete for {label} properties ---")

# --- 3. ML PREPARATION FUNCTIONS ---       
def prepare_for_ml(df):
    #Final step before modeling: Handles Categorical Encoding and Feature Selection.
    # 1. Feature Selection (Only columns that have variety and no NaNs)
    features = ['living_area', 'nb_rooms', 'has_garden', 'has_terrace', 'property_type', 'province', 'postcode', 'facades']
    target = 'price'
    
       
    # 2. Filter and Encode using One-Hot Encoding for categorical variables
    df_ml = df[features + [target]].copy()
    df_ml = pd.get_dummies(df_ml, columns=['property_type', 'province'], drop_first=True)

    """"
    # 3. Ensure Numeric
    # Postcode is already a number from our earlier extraction step
    df_ml['postcode'] = df_ml['postcode'].fillna(0).astype(int)
    """
    return df_ml
    
# --- EXECUTION PIPELINE ---
if __name__ == "__main__":
    RAW_PATH = 'immo_eliza_scraper/results.csv'
    if os.path.exists(RAW_PATH):
        raw_df = pd.read_csv(RAW_PATH)
    
        # 1. Load and Clean
        cleaned_df = clean_immo_data(raw_df)
    
        # 2. Split by Sale/Rent
        df_sale = cleaned_df[cleaned_df['type_of_sale'] == 'sale'].copy() # Adjust based on your goal
        df_rent = cleaned_df[cleaned_df['type_of_sale'] == 'rent'].copy()   # Adjust based on your goal

        # Remove Statistical Outliers separately
        print("\nProcessing Sales...")
        df_sale = remove_outliers_iqr(df_sale, 'price')
        
        print("\nProcessing Rentals...")
        df_rent = remove_outliers_iqr(df_rent, 'price')
    
        # 3. EDA
        run_eda(df_sale, "Sale")
        run_eda(df_rent, "Rent")
    
        # 4. Prepare and Save
        ml_sale = prepare_for_ml(df_sale)
        os.makedirs('data', exist_ok=True)
        ml_sale.to_csv('data/processed_sale_data.csv', index=False)
        print("✅ Pipeline Complete: Data saved to /data/processed_sale_data.csv") 

        ml_rent = prepare_for_ml(df_rent)
        os.makedirs('data', exist_ok=True)
        ml_rent.to_csv('data/processed_rent_data.csv', index=False)
        print("✅ Pipeline Complete: Data saved to /data/processed_rent_data.csv")
    else:
        print(f"Error: Raw data file '{RAW_PATH}' not found. Please run the scraper first.")