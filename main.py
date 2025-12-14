from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pest_engine import PestEngine
from firebase_init import init_firebase   # IMPORTANT

app = FastAPI(title="KrishiSakhi Pest Advisory")

# Initialize engine
engine = PestEngine()


# -------------------------
# STARTUP: Firebase Init
# -------------------------
@app.on_event("startup")
def startup_event():
    init_firebase()
    print("🚀 Application started successfully")


# -------------------------
# REQUEST MODEL
# -------------------------
class PestRequest(BaseModel):
    crops: list[str]
    district: str
    soilType: str
    language: str = "en"   # ✅ MUST be here


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# PEST ANALYSIS API
# -------------------------
@app.post("/pest/analyse")
def analyse_pest(req: PestRequest):
    try:
        print("📥 Pest request:", req.dict())

        alerts = engine.analyse(
            crops=req.crops,
            district=req.district,
            soil=req.soilType,
            lang=req.language
        )

        return {"alerts": alerts}

    except Exception as e:
        print("❌ Pest analyse error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
