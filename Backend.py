from flask import Flask, request, jsonify
import cudf  # RAPIDS GPU-accelerated Pandas alternative
from cuml.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

# Load historical sales data (Assume CSV file stored in 'sales_data.csv')
def load_data():
    df = cudf.read_csv('sales_data.csv')
    return df

# Train the AI model using NVIDIA RAPIDS
def train_model(df):
    X = df[['customer_interactions', 'ad_spend', 'previous_sales']].astype('float32')
    y = df['future_sales'].astype('float32')

    model = LinearRegression()
    model.fit(X, y)
    
    return model

# Load data and train the model once when the server starts
df = load_data()
model = train_model(df)

@app.route('/predict', methods=['POST'])
def predict_sales():
    try:
        # Get input JSON data
        input_data = request.get_json()
        
        # Convert data into a RAPIDS GPU-accelerated DataFrame
        input_df = cudf.DataFrame(input_data)
        
        # Predict future sales using trained model
        predictions = model.predict(input_df.astype('float32'))
        
        # Convert predictions to a list and return as JSON
        return jsonify({'predicted_sales': predictions.tolist()})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
