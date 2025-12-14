from fastapi import FastAPI, HTTPException
from firebase_init import init_firebase
from pest_engine import PestEngine
from firebase_admin import db
import traceback

app = FastAPI()
engine = PestEngine()

@app.on_event("startup")
def start():
    init_firebase()

@app.post("/scan/farmer/{uid}")
def scan(uid: str):
    try:
        engine.run_scan(uid)
        return {"status": "scan_completed"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(400, detail=str(e))
        
@app.post("/pest/scan/{uid}")
def scan_farmer(uid: str, req: ScanRequest):

    if not req.district or not req.soilType or not req.primaryCrop:
        raise HTTPException(400, "Missing farm data")

    alerts = pest_engine.run_scan(
        district=req.district,
        soil=req.soilType,
        primary=req.primaryCrop,
        secondary=req.secondaryCrop,
        lang=req.language
    )

    db.reference(f"pestAlerts/{uid}").set({
        "alerts": alerts
    })

    return {"status": "ok"}


@app.get("/alerts/{uid}")
def alerts(uid: str):
    return db.reference(f"alerts/{uid}").get() or {"alerts": []}


