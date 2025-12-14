from fastapi import FastAPI, HTTPException
from firebase_init import init_firebase
from pest_engine import PestEngine
from models import ScanRequest, PestResponse
from firebase_admin import db

app = FastAPI(title="KrishiSakhi Pest Backend")

engine = PestEngine()


@app.on_event("startup")
def startup():
    init_firebase()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/scan/farmer/{uid}")
def scan_farmer(uid: str, req: ScanRequest):

    if not req.district or not req.soilType:
        raise HTTPException(400, "district & soilType required")

    engine.run_scan(
        uid=uid,
        district=req.district,
        soil=req.soilType,
        lang=req.language
    )

    return {"status": "scan_started"}


@app.get("/alerts/{uid}", response_model=PestResponse)
def get_alerts(uid: str):

    data = db.reference(f"alerts/{uid}").get()

    if not data or "alerts" not in data:
        return {"alerts": []}

    return data
