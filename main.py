from fastapi import FastAPI, HTTPException, Request
from firebase_init import init_firebase
from pest_engine import PestEngine
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
async def scan_farmer(uid: str, request: Request):
    """
    Accept scan request WITH or WITHOUT body.
    This prevents HTTP 400 permanently.
    """
    try:
        body = {}
        try:
            body = await request.json()
        except Exception:
            pass  # no body sent

        lang = body.get("language", "en")

        engine.run_scan(uid=uid, lang=lang)

        return {"status": "scan_completed"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alerts/{uid}")
def get_alerts(uid: str):
    data = db.reference(f"alerts/{uid}").get()
    return data if data else {"alerts": []}
