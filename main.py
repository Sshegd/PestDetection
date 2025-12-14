from fastapi import FastAPI, HTTPException
from firebase_init import init_firebase
from pest_engine import PestEngine
from firebase_admin import db

app = FastAPI()
engine = PestEngine()

@app.on_event("startup")
def startup():
    init_firebase()

@app.post("/scan/farmer/{uid}")
def scan_farmer(uid: str, lang: str = "en"):
    try:
        engine.run_scan(uid, lang)
        return {"status": "scan_completed"}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/alerts/{uid}")
def get_alerts(uid: str):
    data = db.reference(f"alerts/{uid}").get()
    return data if data else {"alerts": []}
