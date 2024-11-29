from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, firestore


# Firebase setup
cred = credentials.Certificate("firebase-key.json")  # Replace with the actual file name if different
firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view')
def view():
    return render_template('view.html')

if __name__ == '__main__':
    app.run(debug=True)