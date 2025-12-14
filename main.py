from fastapi import FastAPI, HTTPException
from firebase_init import init_firebase
from pest_engine import PestEngine
from models import ScanRequest
from firebase_admin import db

app = FastAPI()
engine = PestEngine()


@app.on_event("startup")
def startup():
    init_firebase()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/scan/farmer/{uid}")
def scan_farmer(uid: str, req: ScanRequest | None = None):
    """
    Scan farmer pests.
    Android may send request body OR not.
    """

    try:
        # language priority:
        # 1️⃣ request body
        # 2️⃣ Firebase
        # 3️⃣ default en
        lang = req.language if req and req.language else "en"

        engine.run_scan(uid=uid, lang=lang)

        return {"status": "scan_completed"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/alerts/{uid}")
def get_alerts(uid: str):
    data = db.reference(f"alerts/{uid}").get()
    return data if data else {"alerts": []}
