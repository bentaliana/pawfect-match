import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate("firebase-key.json")  # Replace with the actual file name if different
firebase_admin.initialize_app(cred)
db = firestore.client()