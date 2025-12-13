# main.py
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import firebase_admin
from firebase_admin import credentials, db

from pest_engine import PestEngine
from pest_db import PEST_DB
from district_pest_history import PEST_HISTORY

FIREBASE_CREDS = os.environ.get("FIREBASE_CREDENTIALS")
FIREBASE_DB_URL = os.environ.get("FIREBASE_DB_URL")

if not FIREBASE_CREDS or not FIREBASE_DB_URL:
    raise RuntimeError("Firebase env vars missing")

cred = credentials.Certificate(json.loads(FIREBASE_CREDS))
firebase_admin.initialize_app(cred, {
    "databaseURL": FIREBASE_DB_URL
})

app = FastAPI(title="KrishiSakhi Pest Detection API")

pest_engine = PestEngine(
    pest_db=PEST_DB,
    pest_history=PEST_HISTORY
)

def now_ts_ms():
    return int(time.time() * 1000)


def read_user(uid: str) -> Optional[Dict[str, Any]]:
    return db.reference("Users").child(uid).get()


def store_alert(uid: str, alert: Dict[str, Any]) -> str:
    ref = db.reference(f"alerts/{uid}")
    aid = f"alert_{now_ts_ms()}"
    ref.child(aid).set(alert)
    return aid


def get_user_crops(user: dict) -> List[str]:
    crops = []
    farm = user.get("farmDetails", {})

    if farm.get("primaryCrop"):
        crops.append(farm["primaryCrop"])

    crops.extend(farm.get("secondaryCrops", []))

    return list(set(crops))

def fetch_weather_for_district(district: str) -> Dict[str, float]:
    # You can replace this with real API later
    return {
        "temp": 32.0,
        "humidity": 75.0,
        "rainfall": 12.0
    }

@app.post("/scan/farmer/{uid}")
def scan_farmer(uid: str):

    # -------------------------------
    # 1. LOAD USER
    # -------------------------------
    user = read_user(uid)
    if not user:
        raise HTTPException(404, "Farmer not found")

    farm = user.get("farmDetails", {})
    district = farm.get("district")
    taluk = farm.get("taluk")
    soil_type = farm.get("soilType")
    stage = farm.get("cropStage")

    if not district:
        raise HTTPException(400, "District missing")

    # -------------------------------
    # 2. GET ALL CROPS
    # -------------------------------
    crops = get_user_crops(user)
    if not crops:
        raise HTTPException(400, "No crops found")

    # -------------------------------
    # 3. WEATHER INPUT
    # -------------------------------
    weather = fetch_weather_for_district(district)

    # -------------------------------
    # 4. CLEAR OLD ALERTS
    # -------------------------------
    db.reference(f"alerts/{uid}").delete()

    stored_alerts = []

    # ==================================================
    # 5. RUN PEST ENGINE FOR EACH CROP
    # ==================================================
    for crop in crops:

        pest_results = pest_engine.predict(
            cropName=crop,
            district=district,
            taluk=taluk,
            soilType=soil_type,
            stage=stage,
            temp=weather["temp"],
            humidity=weather["humidity"],
            rainfall=weather["rainfall"],
            month_int=datetime.utcnow().month,
            lang=farm.get("language", "en")
        )

        for p in pest_results:
            alert = {
                "uid": uid,
                "cropName": crop,
                "timestamp": now_ts_ms(),
                "alertType": "pest_detection",
                "pestName": p["pestName"],
                "riskLevel": p["riskLevel"],
                "riskScore": p["score"],
                "reasons": p["reasons"],
                "symptoms": p["symptoms"],
                "preventiveMeasures": p["preventive"],
                "correctiveMeasures": p["corrective"]
            }

            aid = store_alert(uid, alert)
            stored_alerts.append({**alert, "alertId": aid})

    return {
        "status": "ok",
        "totalCrops": len(crops),
        "totalAlerts": len(stored_alerts),
        "alerts": stored_alerts
    }

@app.get("/alerts/{uid}")
def get_alerts(uid: str):
    return db.reference(f"alerts/{uid}").get() or {}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat()
    }
