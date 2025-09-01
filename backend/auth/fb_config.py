import firebase_admin
from firebase_admin import credentials, auth

# Path to service account key
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
