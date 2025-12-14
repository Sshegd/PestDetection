import os, json, firebase_admin
from firebase_admin import credentials, db

def init_firebase():
    if firebase_admin._apps:
        return

    cred = credentials.Certificate(
        json.loads(os.environ["FIREBASE_CREDENTIALS"])
    )

    firebase_admin.initialize_app(cred, {
        "databaseURL": os.environ["FIREBASE_DB_URL"]
    })
