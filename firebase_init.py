import os
import json
import firebase_admin
from firebase_admin import credentials, db

def init_firebase():
    if firebase_admin._apps:
        return

    cred_json = os.getenv("FIREBASE_CREDENTIALS")
    db_url = os.getenv("FIREBASE_DB_URL")

    if not cred_json:
        raise RuntimeError("FIREBASE_CREDENTIALS not set")

    if not db_url:
        raise RuntimeError("FIREBASE_DB_URL not set")

    cred_dict = json.loads(cred_json)

    cred = credentials.Certificate(cred_dict)

    firebase_admin.initialize_app(cred, {
        "databaseURL": db_url
    })

    print("✅ Firebase initialized")
