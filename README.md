# Project Title

## Project Overview

This project is designed to generate descriptions for pet adoption using machine learning models. It includes various components such as data preprocessing, model training, and a web interface for generating and viewing descriptions.

## Project Structure

```
.
├── pycache/
├── .gitignore
├── ai_server.py
├── app.py
├── colab files/
│   ├── CLIP_SWE.ipynb
│   ├── desc_gen_final.ipynb
│   ├── Machine_translation_final.ipynb
├── config.py
├── cors.json
├── docker-compose.yml
├── Dockerfile.artint
├── Dockerfile.interface
├── Dockerfile.orchestration
├── firebase-key.json
├── flan_t5_trained_model/
│   ├── added_tokens.json
│   ├── config.json
│   ├── generation_config.json
│   ├── model.safetensors
│   ├── special_tokens_map.json
│   ├── spiece.model
├── flan_t5_trained_model_old/
├── orchestration_server.py
├── README.md
├── requirements.txt
├── static/
│   ├── css/
│   │   ├── styles.css
│   ├── images/
│   ├── script.js
├── templates/
│   ├── home.html


```

## Folder and File Descriptions

- `__pycache__/`: Contains compiled Python files.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `ai_server.py`: Contains the AI server implementation.
- `app.py`: Main application file to run the web server.
- `colab files/`: Contains Jupyter notebooks for various tasks.
  - `CLIP_SWE.ipynb`: Notebook for CLIP model.
  - `desc_gen_final.ipynb`: Notebook for description generation.
  - `Machine_translation_final.ipynb`: Notebook for machine translation.
- `config.py`: Configuration file for the project.
- `cors.json`: Configuration for Cross-Origin Resource Sharing.
- `docker-compose.yml`: Docker Compose configuration file.
- `Dockerfile.artint`: Dockerfile for the AI component.
- `Dockerfile.interface`: Dockerfile for the web interface.
- `Dockerfile.orchestration`: Dockerfile for orchestration.
- `firebase-key.json`: Firebase service account key.(SENT BY EMAIL)
- `flan_t5_trained_model/`: Contains the trained FLAN-T5 model files. (CAN BE FOUND ON DRIVE)
  - `added_tokens.json`, `config.json`, `generation_config.json`, `model.safetensors`, `special_tokens_map.json`, `spiece.model`: Model files.
- `flan_t5_trained_model_old/`: Contains old versions of the trained model.
- `orchestration_server.py`: Contains the orchestration server implementation.
- `README.md`: This file.
- `requirements.txt`: Lists the Python dependencies.
- `static/`: Contains static files for the web interface.
  - `css/`: Contains CSS files.
    - `styles.css`: Main stylesheet.
  - `images/`: Contains image files.
  - `script.js`: Main JavaScript file.
- `templates/`: Contains HTML templates.
  - `home.html`: Main HTML template for the home page.

## How to Run

### Prerequisites

- Docker
- Docker Compose
- Python 3.9

### Steps

1. **Clone the repository:**

   ```sh
   git clone https://github.com/alisonattard/pawfect-match.git
   cd <repository-directory>
   ```

2. **Set up the environment:**
   Ensure you have the firebase-key.json to read/write from/to Firebase.
   Ensure you have the flan_t5_trained_model folder.

3. **Build and run the Docker containers:**
   Ensure Docker/Docker-Compose are installed.
   Run the following to build the project:
   ```
   docker-compose up --build
   ```
