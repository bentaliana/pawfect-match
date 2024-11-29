from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AI_SERVER_URL = "http://ai_server:6000"

@app.route('/predict_image_keywords', methods=['POST'])
def predict_image_keywords():
    try:
        response = requests.post(f"{AI_SERVER_URL}/predict_image_keywords", files=request.files)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_description', methods=['POST'])
def generate_description():
    try:
        response = requests.post(f"{AI_SERVER_URL}/generate_description", json=request.json)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate():
    try:
        response = requests.post(f"{AI_SERVER_URL}/translate", json=request.json)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)