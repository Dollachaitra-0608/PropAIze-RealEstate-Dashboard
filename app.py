# Flask backend for Real Estate Dashboard with ML price prediction
from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load trained model and encoders
print("[v0] Loading ML model...")
with open('model.pkl', 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']
    le_city = model_data['le_city']
    le_type = model_data['le_type']

# Load dataset for analytics
df = pd.read_csv('data.csv')
print("[v0] ML model loaded successfully")

# Route to serve the dashboard
@app.route('/')
def index():
    """Serve the main dashboard HTML"""
    return render_template('index.html')

# Route to get analytics data
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Return dashboard analytics data"""
    try:
        # Calculate summary statistics
        total_listings = len(df)
        avg_price = df['price'].mean()
        min_price = df['price'].min()
        max_price = df['price'].max()
        
        # City-wise distribution
        city_stats = df.groupby('city').agg({
            'price': ['mean', 'count']
        }).round(2)
        
        city_data = []
        for city in city_stats.index:
            city_data.append({
                'city': city,
                'avg_price': float(city_stats.loc[city, ('price', 'mean')]),
                'count': int(city_stats.loc[city, ('price', 'count')])
            })
        
        # Price trends (sorted by area)
        df_sorted = df.sort_values('area')
        price_trends = [
            {'area': int(row['area']), 'price': float(row['price'])}
            for _, row in df_sorted.iterrows()
        ]
        
        response = {
            'total_listings': total_listings,
            'avg_price': float(avg_price),
            'min_price': float(min_price),
            'max_price': float(max_price),
            'city_data': city_data,
            'price_trends': price_trends
        }
        return jsonify(response)
    except Exception as e:
        print(f"[v0] Error in analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Route for price prediction
@app.route('/api/predict', methods=['POST'])
def predict_price():
    """Predict property price using ML model"""
    try:
        data = request.get_json()
        
        # Extract features
        area = float(data.get('area', 0))
        bedrooms = int(data.get('bedrooms', 0))
        bathrooms = int(data.get('bathrooms', 0))
        city = data.get('city', '')
        property_type = data.get('property_type', '')
        
        # Validate inputs
        if not all([area, bedrooms, bathrooms, city, property_type]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Encode categorical variables
        city_encoded = le_city.transform([city])[0]
        type_encoded = le_type.transform([property_type])[0]
        
        # Prepare features for prediction
        features = np.array([[area, bedrooms, bathrooms, city_encoded, type_encoded]])
        
        # Make prediction
        predicted_price = model.predict(features)[0]
        
        # Round to 2 decimal places
        predicted_price = round(predicted_price, 2)
        
        print(f"[v0] Prediction made: Area={area}, BR={bedrooms}, BA={bathrooms}, City={city}, Type={property_type} -> Price=${predicted_price}")
        
        return jsonify({
            'predicted_price': predicted_price,
            'input_data': {
                'area': area,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'city': city,
                'property_type': property_type
            }
        })
    except ValueError as e:
        print(f"[v0] Validation error: {str(e)}")
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        print(f"[v0] Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Route not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("[v0] Starting Flask server...")
    # Use debug=True for development, debug=False for production
    app.run(debug=True, host='0.0.0.0', port=5000)
