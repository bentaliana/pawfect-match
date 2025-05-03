from flask import Flask, request, jsonify
from PIL import Image
import torch
import clip  # OpenAI's CLIP library
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, MarianMTModel, MarianTokenizer
from sklearn.metrics.pairwise import cosine_similarity
from huggingface_hub import login
import numpy as np
import requests

# Initialize Flask app
app = Flask(__name__)

# Load the CLIP model for image-to-text prediction
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = clip.load("ViT-B/32", device=device)

# Login to HuggingFace
login("REDACTED")

# Load the FLAN-T5 model (for description generation)
FLAN_MODEL_PATH = "Alexandra26/SE_t5"
flan_tokenizer = AutoTokenizer.from_pretrained(FLAN_MODEL_PATH)
flan_model = AutoModelForSeq2SeqLM.from_pretrained(FLAN_MODEL_PATH).to(device)

# Load Model 2 (for Machine translation)
MODEL_2_PATH = "Alexandra26/SE_project"
marian_tokenizer = MarianTokenizer.from_pretrained(MODEL_2_PATH)
marian_model = MarianMTModel.from_pretrained(MODEL_2_PATH)

# Predefined lists of animals and general keywords
animals = ["cat", "dog"]
keywords_list = ["small", "fluffy", "sleek", "spotted", "striped", "soft", "shiny", "bright-eyed", "whiskered", "short-haired", "long-haired"]

# Image-to-description prediction route (using CLIP)
@app.route('/predict_image_keywords', methods=['POST'])
def predict_image_keywords():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    
    try:
        # Open image using PIL
        image = Image.open(image_file.stream)

        # Preprocess image using CLIP
        image_input = preprocess(image).unsqueeze(0).to(device)

        # Get image features from CLIP model
        with torch.no_grad():
            image_features = clip_model.encode_image(image_input)

        # Convert image features to numpy
        image_features = image_features.cpu().numpy()

        # Combine animals and general keywords into a single list
        all_keywords = animals + keywords_list

        # Encode all keywords (text) using CLIP model
        text_inputs = clip.tokenize(all_keywords).to(device)
        with torch.no_grad():
            text_features = clip_model.encode_text(text_inputs)

        # Convert text features to numpy
        text_features = text_features.cpu().numpy()

        # Calculate cosine similarity between image features and keyword features
        similarities = cosine_similarity(image_features, text_features)

        # Separate similarities for animals and other keywords
        animal_similarities = similarities[0, :len(animals)]
        keyword_similarities = similarities[0, len(animals):]

        # Get the best matching animal
        best_animal_index = np.argmax(animal_similarities)
        best_animal = animals[best_animal_index]

        # Get the top 3 additional keywords (excluding animals)
        top_keyword_indices = np.argsort(keyword_similarities)[-3:][::-1]
        top_keywords = [keywords_list[i] for i in top_keyword_indices]

        # Combine the best animal with the top additional keywords
        final_keywords = [best_animal] + top_keywords

        # Call the generate_description function with the keywords as prompt
        description = generate_description(final_keywords)

        # Return the generated description
        result = {"message": "Prediction successful", "description": description}

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Generate description (using FLAN-T5)
@app.route('/generate_description', methods=['POST'])
def generate_description():
    if not request.json or 'prompt' not in request.json:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        # Get the prompt from the request
        prompt = request.json['prompt']

        # Tokenize the input prompt
        inputs = flan_tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)

        # Generate the description using FLAN-T5
        outputs = flan_model.generate(**inputs, max_length=130, num_beams=5, early_stopping=True, 
                                      repetition_penalty=1.8, temperature=1.2, length_penalty=1.2, 
                                      do_sample=True, top_k=30, top_p=0.9)

        # Decode the generated description
        description = flan_tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Return the generated description
        return jsonify({"description": description})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Machine translation (using MarianMT)
@app.route('/translate', methods=['POST'])
def translate():
    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Get the text input for translation
        text = request.json['text']

        # Tokenize the input text for MarianMT
        inputs = marian_tokenizer(text, return_tensors="pt", padding=True, truncation=True)

        # Translate the text using MarianMT
        translated = marian_model.generate(**inputs)

        # Decode the translated text
        translation = marian_tokenizer.decode(translated[0], skip_special_tokens=True)

        # Return the translated text
        return jsonify({"translation": translation})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Helper function to generate description
def generate_description(keywords):
    prompt = "Generate an engaging and lively pet adoption description. Highlight the pet's best traits and personality while making it irresistible for adoption. Use the following characteristics: " + " ".join(keywords)
    
    # Tokenize the input prompt
    inputs = flan_tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)

    # Generate the description using FLAN-T5
    outputs = flan_model.generate(**inputs, max_length=130, num_beams=5, early_stopping=True, 
                                  repetition_penalty=1.8, temperature=1.2, length_penalty=1.2, 
                                  do_sample=True, top_k=10, top_p=0.8)

    # Decode the generated description
    description = flan_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return description


# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)