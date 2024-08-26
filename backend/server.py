from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import joblib
import pandas as pd
from io import StringIO
from datetime import datetime

app = Flask(__name__)
CORS(app) # enable routes for all routes

model = joblib.load('../model/model.joblib')

def predict_input(input_df):
    # load the model
    model_from_disk = model
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
    print(f"Received arguments: {args}")

    command = [
        r"C:\Users\Gaby\anaconda3\envs\arcgis_env\python.exe", # Windows
        #'/home/ubuntu/miniconda3/envs/arcgis_env/bin/python3',  # Linux, Full path to Python in the conda environment
        'Arcgis/CurrentWeatherData.py'
    ] + args

    if (len(args) == 4):
        try:
            print("Running the weather script")
            # Run the weather script with arguments
            result = subprocess.run(command, capture_output=True, text=True)

            print("Subprocess finished with return code:", result.returncode)
            print("Standard Output:", result.stdout)
            print("Standard Error:", result.stderr)

            if result.returncode == 0:
                df = pd.read_csv(StringIO(result.stdout))
                print(df)

                df_json = df.to_json(orient='records')

                print("Feeding the data to the AI")

                # Feed it to the AI and get the outputs
                prediction, probability = predict_input(df)

                print("Returning the output...")

                prediction = str(prediction)
                probability = str(probability)

                # Return the results as a JSON
                return jsonify({
                    'prediction': prediction,
                    'probability': probability,
                    'weather': df_json
                })
        
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
        
# @app.route('/get-fires', methods=['GET'])
# def get_fires():
#     old_df = pd.read_csv("data/2000-2021_fires+weather.csv")
#     old_json = old_df.to_json(orient='records')

#     live_df = pd.read_csv("Arcgis/data/Active_Fires.csv")
#     live_json = live_df.to_json(orient='records')

#     return jsonify({
#         'old': old_json,
#         'live': live_json
#     })

@app.route('/get-fires', methods=['POST'])
def get_fires():

    # Extract arguments from the request
    args = request.json.get('args', [])
    print(f"Received arguments: {args}")

    if (len(args) == 2):
        try:
            start_date = args[0]
            end_date = args[1]

            dt_start = datetime.strptime(start_date, '%d-%m-%Y')
            dt_end = datetime.strptime(end_date, '%d-%m-%Y')

            old_df = pd.read_csv("data/2000-2021_fires+weather.csv")
            old_df_date = pd.to_datetime(old_df['date'])
            old_filtered_df = old_df[(old_df_date >= dt_start) & (old_df_date <= dt_end)]
            old_filtered_json = old_filtered_df.to_json(orient='records')

            live_df = pd.read_csv("Arcgis/data/Active_Fires.csv")
            live_df_date = pd.to_datetime(live_df['date'])
            live_filtered_df = live_df[(live_df_date >= dt_start) & (live_df_date <= dt_end)]
            live_filtered_json = live_filtered_df.to_json(orient='records')

            return jsonify({
                'old': old_filtered_json,
                'live': live_filtered_json
            })
        
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)