from flask import Flask, render_template, request, jsonify
from config import db  # Import the Firebase configuration
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

ORCHESTRATION_SERVER_URL = "http://orchestration_server:7000"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/predict_image_keywords', methods=['POST'])
def predict_image_keywords():
    response = requests.post(f"{ORCHESTRATION_SERVER_URL}/predict_image_keywords", files=request.files)
    return jsonify(response.json())

@app.route('/generate_description', methods=['POST'])
def generate_description():
    response = requests.post(f"{ORCHESTRATION_SERVER_URL}/generate_description", json=request.json)
    return jsonify(response.json())

@app.route('/translate', methods=['POST'])
def translate():
    response = requests.post(f"{ORCHESTRATION_SERVER_URL}/translate", json=request.json)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)