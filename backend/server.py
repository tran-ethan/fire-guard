from flask import Flask, render_template, request, jsonify
import subprocess
import json
import requests

app = Flask(__name__)

@app.route("/") # default endpoint
def index():
    return render_template("index.html")

@app.route('/fire-analysis', methods=['POST'])
def fire_analysis():
    
        # Extract arguments from the request if needed
        args = request.json.get('args', [])

        if (len(args) == 2):
            try:
                # Run the weather script with arguments
                subprocess.run(['python3', 'Arcgis/data/WeatherData.py'] + args, capture_output=True, text=True)

                # Feed the result to the AI

                # Return the output
                
                # # Return the output of the script
                # return jsonify({
                #     'status': 'success',
                #     'output': result.stdout
                # })
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)