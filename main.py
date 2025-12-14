from fastapi import FastAPI, HTTPException, Request
from firebase_init import init_firebase
from pest_engine import PestEngine
from firebase_admin import db
import traceback

app = FastAPI()
engine = PestEngine()

@app.on_event("startup")
def startup():
    init_firebase()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/scan/farmer/{uid}")
async def scan_farmer(uid: str, request: Request):
    try:
        body = {}
        try:
            body = await request.json()
        except Exception:
            pass

        lang = body.get("language", "en")

        # 🔥 THIS IS WHERE 400 IS COMING FROM
        engine.run_scan(uid=uid, lang=lang)

        return {"status": "scan_completed"}

    except Exception as e:
        # 🔥 LOG FULL ERROR
        print("SCAN ERROR:", str(e))
        traceback.print_exc()

        # 🔥 RETURN ERROR TEXT TO ANDROID
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.get("/alerts/{uid}")
def get_alerts(uid: str):
    data = db.reference(f"alerts/{uid}").get()
    return data if data else {"alerts": []}
