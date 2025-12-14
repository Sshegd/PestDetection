from fastapi import FastAPI, HTTPException
from firebase_init import init_firebase
from firebase_admin import db
from models import ScanRequest   # ✅ FIX
import traceback

app = FastAPI()

@app.on_event("startup")
def start():
    init_firebase()

@app.post("/scan/farmer/{uid}")
def scan_farmer(uid: str, req: ScanRequest):

    try:
        if not req.district or not req.soilType or not req.primaryCrop:
            raise ValueError("Incomplete scan request")

        # SIMPLE STATIC RESPONSE FOR TESTING
        alerts = [{
            "crop": req.primaryCrop,
            "pest": "Root Grub",
            "risk": "High",
            "symptoms": "Yellowing leaves",
            "preventive": "Good drainage",
            "treatment": "Soil insecticide"
        }]

        db.reference(f"alerts/{uid}").set({"alerts": alerts})

        return {"status": "scan_completed"}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/alerts/{uid}")
def get_alerts(uid: str):
    data = db.reference(f"alerts/{uid}").get()

    if not data or not isinstance(data, dict):
        return {"alerts": []}

    alerts = data.get("alerts", [])
    if not isinstance(alerts, list):
        return {"alerts": []}

    return {"alerts": alerts}




