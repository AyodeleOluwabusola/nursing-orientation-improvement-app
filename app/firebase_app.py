# app/firebase_app.py
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("secrets/firebase-service-account.json")
firebase_app = firebase_admin.initialize_app(cred)
