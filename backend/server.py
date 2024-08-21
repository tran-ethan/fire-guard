from flask import Flask, render_template, request, jsonify
import sklearn
import subprocess
import joblib
import pandas as pd
import numpy

app = Flask(__name__)

model_from_disk = joblib.load('../model/model.joblib')

def predict_input(input_df):
    # Get columns
    input_columns = model_from_disk['input_cols']
    # Make month column
    input_df['date'] = pd.to_datetime(input_df['date'])
    input_df['month'] = input_df['date'].dt.month
    # Run scaler on input columns
    input_df[input_columns] = model_from_disk['scaler'].transform(input_df[input_columns])
    x_input = input_df[input_columns]
    prediction = model_from_disk['model'].predict(x_input)[0]
    probability = model_from_disk['model'].predict_proba(x_input)[0][list(model_from_disk['model'].classes_).index(prediction)]
    return prediction, probability

@app.route("/") # default endpoint
def index():
    return render_template("index.html")

@app.route('/fire-analysis', methods=['POST'])
def fire_analysis():
    
    # Extract arguments from the request
    args = request.json.get('args', [])
    args_str = ' '.join(args)  # Convert list to string

    command = [
        '/home/ubuntu/miniconda3/envs/arcgis_env/bin/python3',  # Full path to Python in the conda environment
        'Arcgis/CurrentWeatherData.py'
    ] + args_str

    if (len(args) == 4):
        try:
            # Run the weather script with arguments
            df = subprocess.run(command, capture_output=True, text=True)

            # Feed it to the AI and get the outputs
            prediction, probability = predict_input(df)

            # Return the results as JSON
            return jsonify({
                'prediction': prediction,
                'probability': probability
            })
        
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)