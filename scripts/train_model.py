# Script to create sample dataset and train ML model for price prediction
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Set random seed for reproducibility
np.random.seed(42)

# Create sample dataset
print("[v0] Creating sample dataset...")
data = {
    'area': np.random.randint(500, 5000, 100),
    'bedrooms': np.random.randint(1, 6, 100),
    'bathrooms': np.random.randint(1, 4, 100),
    'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], 100),
    'property_type': np.random.choice(['House', 'Apartment', 'Condo'], 100),
}

df = pd.DataFrame(data)

# Generate realistic prices based on features
# Formula: base_price + area_factor + bedroom_factor + city_factor
city_prices = {
    'New York': 500000,
    'Los Angeles': 450000,
    'Chicago': 300000,
    'Houston': 250000,
    'Phoenix': 280000
}

df['price'] = df.apply(
    lambda row: city_prices[row['city']] + 
                (row['area'] * 100) + 
                (row['bedrooms'] * 50000) + 
                (row['bathrooms'] * 30000) +
                np.random.randint(-50000, 50000),
    axis=1
)

# Save to CSV
df.to_csv('data.csv', index=False)
print(f"[v0] Dataset created: {len(df)} records saved to data.csv")
print(f"[v0] Sample data:\n{df.head()}")

# Prepare data for training
print("\n[v0] Preparing data for ML model training...")
X = df[['area', 'bedrooms', 'bathrooms']].copy()

# Encode categorical variables
le_city = LabelEncoder()
le_type = LabelEncoder()
X['city_encoded'] = le_city.fit_transform(df['city'])
X['type_encoded'] = le_type.fit_transform(df['property_type'])

y = df['price']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
print("[v0] Training Random Forest model...")
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluate model
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"[v0] Model Training Score: {train_score:.4f}")
print(f"[v0] Model Test Score: {test_score:.4f}")

# Save model and encoders
print("[v0] Saving model and encoders...")
with open('model.pkl', 'wb') as f:
    pickle.dump({
        'model': model,
        'le_city': le_city,
        'le_type': le_type
    }, f)

print("[v0] Model training complete! Files saved: data.csv, model.pkl")
