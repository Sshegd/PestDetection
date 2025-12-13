# main.py
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import firebase_admin
from firebase_admin import credentials, db, messaging

try:
    import joblib
except Exception:
    joblib = None

# -------------------------
# Config / Env
# -------------------------
FIREBASE_CREDS = os.environ.get("FIREBASE_CREDENTIALS")
FIREBASE_DB_URL = os.environ.get("FIREBASE_DB_URL")
WEATHER_API_URL = os.environ.get("WEATHER_API_URL")  # Provider endpoint (e.g. Open-Meteo)
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")  # optional
ML_MODEL_PATH = os.environ.get("ML_MODEL_PATH")     # optional (joblib model)

if not FIREBASE_CREDS or not FIREBASE_DB_URL:
    raise RuntimeError("Set FIREBASE_CREDENTIALS and FIREBASE_DB_URL environment variables")

cred = credentials.Certificate(json.loads(FIREBASE_CREDS))
firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_DB_URL})

app = FastAPI(title="Pest Detection + Synonyms + Kannada + ML + Weather", version="1.0")

LOOKBACK_DAYS = 14
# -----------------------------------------------------
# Render-Compatible Firebase Initialization
# -----------------------------------------------------
# -------------------------
# District -> lat/lon mapping (add more as needed)
# Use approximate coordinates for district HQs / representative locations.
# -------------------------
DISTRICT_COORDS = {
    "uttara kannada": {"lat": 14.6167, "lon": 74.5833},  # Karwar area
    "shimoga": {"lat": 13.9299, "lon": 75.5681},        # Shivamogga
    "dharwad": {"lat": 15.4589, "lon": 75.0078},
    "mysuru": {"lat": 12.2958, "lon": 76.6394},
    "bangalore rural": {"lat": 12.9538, "lon": 77.3500},
    "udupi": {"lat": 13.3409, "lon": 74.7421},
    # add your districts...
}# -----------------------------------------------------
# -------------------------
# Pest synonyms (eng -> list of synonyms incl. Kannada names)
# Extend as you learn local names. Use lowercase.
# -------------------------
# -------------------------
# Kannada translations for common keys & messages (extend as needed)
# -------------------------
KANANDA_TRANSLATIONS = {
    # keys
    "riskScore": "ರಿಸ್ಕ್ ಸ್ಕೋರ್",
    "severity": "ತೀವ್ರತೆ",
    "complexityLevel": "ಸಂಕೀರ್ಣತೆ ಮಟ್ಟ",
    "preventiveMeasures": "ರಕ್ಷಕ ಕ್ರಮಗಳು",
    "correctiveMeasures": "ಶಿಕ್ಷಣಾತ್ಮಕ ಕ್ರಮಗಳು",
    "triggerPest": "ಪ್ರೇರಣ ಕೀಟ/ರೋಗ",
    "reasons": "ಕಾರಣಗಳು",
    # severity values
    "low": "ಕಡಿಮೆ",
    "moderate": "ಮಧ್ಯಮ",
    "high": "ಹೆಚ್ಚು",
    # complexity
    "simple": "ಸಾದಾ",
    "moderate": "ಮಧ್ಯಮ",
    "complex": "ಸಂಕೀರ್ಣ",
    "critical": "ಗಂಭೀರ",
    # measures (examples — these will be reused, translated where straightforward)
    "Scout fields daily": "ಪ್ರತಿ ದಿನ ಕ್ಷೇತ್ರವನ್ನು ತಪಾಸಣೆ ಮಾಡಿ",
    "Maintain hygiene": "ಶುದ್ಧತೆ ಯನ್ನು ಕಾಯ್ದುಕೊಳ್ಳಿ",
    "Use IPM": "IPM ವಿಧಾನಗಳನ್ನು ಉಪಯೋಗಿಸಿ",
    "Consult extension officer": "ವಿಸ್ತರಣಾ ಅಧಿಕಾರಿಗೆ ಸಂಪರ್ಕಿಸಿ",
    "Use approved inputs only": "ಹೇಷಿದ ಪರಿಕರಗಳನ್ನು ಮಾತ್ರ ಬಳಸಿ"
}
PEST_SYNONYMS = {
    "thrips": ["thrips", "kakki", "ಥ್ರಿಪ್ಸ್", "thrip"],
    "aphid": ["aphid", "shikara", "aphids", "ಏಫಿಡ್"],
    "powdery_mildew": ["powdery mildew", "powdery", "udupu haigalu", "powdery_mildew"],
    "whitefly": ["whitefly", "white fly", "ಬೆಳ್ಳುಪೂಸು"],
    "mite": ["mite", "mites", "ನೋಡುಮಟ್ಟಿ"],
    "fruit_fly": ["fruit fly", "fruit_fly", "ಹಣ್ಣು ಕೀಟ"],
    "mosaic_virus": ["mosaic", "virus", "ಮೋಸಾಯಿಕ್"],
    # add more synonyms
}
# -----------------------------------------------------
# ICAR / Govt Report Model
# -----------------------------------------------------
class PestReport(BaseModel):
    reportId: str
    district: str
    crop: str
    pest: Optional[str] = None
    symptoms: Optional[str] = None
    confidence: Optional[float] = 1.0
    reportDate: Optional[str] = None


CROP_DB = {
    # ---------------------------------------------
    # 1. CHILLI
    # ---------------------------------------------
    "chilli": {
        "thrips": {
            "preventive": [
                "Use blue sticky traps (40 per acre).",
                "Avoid excess nitrogen application.",
                "Maintain crop spacing for air circulation.",
                "Remove nearby alternate host weeds."
            ],
            "corrective": [
                "Spray neem oil 3%.",
                "Use Beauveria bassiana bio-control.",
                "If severe, use recommended insecticide as per local extension guidelines."
            ]
        },
        "mosaic_virus": {
            "preventive": [
                "Use virus-free certified seeds.",
                "Control aphid/thrips vectors.",
                "Keep field weed-free.",
                "Use reflective mulches to reduce vector landing."
            ],
            "corrective": [
                "Remove infected plants immediately.",
                "Spray neem oil to reduce vectors.",
                "Avoid planting near older infected fields."
            ]
        }
    },

    # ---------------------------------------------
    # 2. CUCUMBER
    # ---------------------------------------------
    "cucumber": {
        "aphid": {
            "preventive": [
                "Use yellow sticky traps.",
                "Encourage natural predators like ladybird beetles.",
                "Avoid over-irrigation and excess nitrogen."
            ],
            "corrective": [
                "Apply neem oil 5ml/litre.",
                "Introduce Chrysoperla biological predators.",
                "Use systemic insecticide only if infestation is very severe."
            ]
        },
        "powdery_mildew": {
            "preventive": [
                "Use resistant varieties.",
                "Ensure proper spacing and airflow.",
                "Avoid overhead irrigation."
            ],
            "corrective": [
                "Apply wettable sulfur.",
                "Use Trichoderma-based bio fungicides.",
            ]
        }
    },

    # ---------------------------------------------
    # 3. TOMATO
    # ---------------------------------------------
    "tomato": {
        "fruit_borer": {
            "preventive": [
                "Install pheromone traps (Helilure).",
                "Remove damaged fruits regularly.",
                "Use bird perches to attract predators."
            ],
            "corrective": [
                "Release Trichogramma chilonis egg parasitoids.",
                "Spray neem seed kernel extract (NSKE).",
                "Use selective insecticides only if severe."
            ]
        },
        "early_blight": {
            "preventive": [
                "Use resistant varieties.",
                "Maintain proper spacing.",
                "Apply balanced fertilizers."
            ],
            "corrective": [
                "Use copper-based fungicides.",
                "Apply Trichoderma viride as soil treatment."
            ]
        }
    },

    # ---------------------------------------------
    # 4. BRINJAL
    # ---------------------------------------------
    "brinjal": {
        "shoot_and_fruit_borer": {
            "preventive": [
                "Use pheromone traps (20 per acre).",
                "Remove damaged shoots & fruits regularly.",
                "Grow resistant varieties."
            ],
            "corrective": [
                "Release Trichogramma chilonis.",
                "Apply NSKE 5%.",
                "Use chemical insecticides responsibly only for heavy infestation."
            ]
        },
        "whitefly": {
            "preventive": [
                "Use yellow sticky traps.",
                "Maintain weed-free environment."
            ],
            "corrective": [
                "Neem oil 3%.",
                "Use recommended systemic insecticide if severe."
            ]
        }
    },

    # ---------------------------------------------
    # 5. ONION
    # ---------------------------------------------
    "onion": {
        "thrips": {
            "preventive": [
                "Maintain field hygiene.",
                "Use reflective mulches.",
            ],
            "corrective": [
                "Spray neem oil.",
                "Use recommended insecticides responsibly."
            ]
        },
        "purple_blotch": {
            "preventive": [
                "Ensure proper drainage.",
                "Use resistant varieties."
            ],
            "corrective": [
                "Apply mancozeb/copper fungicides per label.",
                "Improve ventilation."
            ]
        }
    },

    # ---------------------------------------------
    # 6. POTATO
    # ---------------------------------------------
    "potato": {
        "late_blight": {
            "preventive": [
                "Use certified seeds.",
                "Avoid overhead irrigation.",
                "Plant in well-drained soils."
            ],
            "corrective": [
                "Fungicide sprays recommended by extension.",
                "Destroy infected plants."
            ]
        }
    },

    # ---------------------------------------------
    # 7. GINGER
    # ---------------------------------------------
    "ginger": {
        "rhizome_rot": {
            "preventive": [
                "Use disease-free planting material.",
                "Ensure proper drainage.",
                "Apply Trichoderma in pits."
            ],
            "corrective": [
                "Remove affected plants.",
                "Improving field drainage.",
                "Apply bio-fungicides."
            ]
        }
    },

    # ---------------------------------------------
    # 8. TURMERIC
    # ---------------------------------------------
    "turmeric": {
        "leaf_blotch": {
            "preventive": [
                "Use healthy seed rhizomes.",
                "Avoid water stagnation.",
                "Maintain adequate spacing."
            ],
            "corrective": [
                "Spray recommended fungicide.",
                "Apply Trichoderma as soil drench."
            ]
        }
    },

    # ---------------------------------------------
    # 9. ARECANUT
    # ---------------------------------------------
    "areca nut": {
        "mite": {
            "preventive": [
                "Maintain irrigation.",
                "Monitor regularly."
            ],
            "corrective": [
                "Apply recommended miticide.",
                "Remove infected tissue."
            ]
        },
        "root_rot": {
            "preventive": [
                "Improve drainage.",
                "Avoid waterlogging."
            ],
            "corrective": [
                "Apply Bordeaux mixture.",
                "Use Trichoderma around roots."
            ]
        }
    },

    # ---------------------------------------------
    # 10. BANANA
    # ---------------------------------------------
    "banana": {
        "sigatoka_leaf_spot": {
            "preventive": [
                "Use disease-free suckers.",
                "Maintain field hygiene.",
                "Ensure proper spacing."
            ],
            "corrective": [
                "Apply copper fungicides.",
                "Remove infected leaves."
            ]
        },
        "rhizome_weevil": {
            "preventive": [
                "Use clean planting material.",
                "Trap adult beetles."
            ],
            "corrective": [
                "Use approved insecticide treatment.",
            ]
        }
    },

    # ---------------------------------------------
    # 11. COCONUT
    # ---------------------------------------------
    "coconut": {
        "eriophyid_mite": {
            "preventive": [
                "Maintain tree health.",
                "Avoid nutrient deficiency."
            ],
            "corrective": [
                "Apply neem oil emulsions.",
                "Use recommended miticides."
            ]
        }
    },

    # ---------------------------------------------
    # 12. COFFEE
    # ---------------------------------------------
    "coffee": {
        "berry_borer": {
            "preventive": [
                "Shade regulation.",
                "Sanitation harvest."
            ],
            "corrective": [
                "Use recommended borer traps.",
                "Destroy infested berries."
            ]
        }
    },

    # ---------------------------------------------
    # 13. PEPPER
    # ---------------------------------------------
    "pepper": {
        "wilt": {
            "preventive": [
                "Use disease-free vines.",
                "Provide proper drainage."
            ],
            "corrective": [
                "Apply Trichoderma.",
                "Remove wilted vines."
            ]
        }
    },

    # ---------------------------------------------
    # 14. CARDAMOM
    # ---------------------------------------------
    "cardamom": {
        "thrips": {
            "preventive": [
                "Shade management.",
                "Maintain humidity."
            ],
            "corrective": [
                "Spray neem oil.",
                "Use recommended insecticide selectively."
            ]
        }
    },

    # ---------------------------------------------
    # 15. MANGO
    # ---------------------------------------------
    "mango": {
        "hoppers": {
            "preventive": ["Sanitation", "Prune for airflow"],
            "corrective": ["Neem oil spray", "Use recommended insecticide"]
        },
        "powdery_mildew": {
            "preventive": ["Maintain spacing", "Use resistant varieties"],
            "corrective": ["Sulfur sprays", "Bio-fungicides"]
        }
    },

    # ---------------------------------------------
    # 16. POMEGRANATE
    # ---------------------------------------------
    "pomegranate": {
        "bacterial_blight": {
            "preventive": ["Use disease-free seedlings", "Prune regularly"],
            "corrective": ["Copper oxychloride spray", "Remove infected branches"]
        }
    },

    # ---------------------------------------------
    # 17. GRAPES
    # ---------------------------------------------
    "grapes": {
        "downy_mildew": {
            "preventive": ["Avoid overhead irrigation", "Maintain airflow"],
            "corrective": ["Apply metalaxyl-based fungicide", "Use Trichoderma"]
        }
    },

    # ---------------------------------------------
    # 18. PADDY (RICE)
    # ---------------------------------------------
    "paddy": {
        "blast": {
            "preventive": ["Use resistant varieties", "Balanced fertilization"],
            "corrective": ["Apply tricyclazole", "Improve drainage"]
        },
        "stem_borer": {
            "preventive": ["Avoid staggered planting", "Use pheromone traps"],
            "corrective": ["Release Trichogramma", "Selective insecticides"]
        }
    },

    # ---------------------------------------------
    # 19. RAGI (FINGER MILLET)
    # ---------------------------------------------
    "ragi": {
        "blast": {
            "preventive": ["Use seed treatment", "Proper spacing"],
            "corrective": ["Fungicide spray", "Rotate crops"]
        }
    },

    # ---------------------------------------------
    # 20. MAIZE
    # ---------------------------------------------
    "maize": {
        "fall_armyworm": {
            "preventive": ["Early sowing", "Use pheromone traps"],
            "corrective": ["Neem oil spray", "Use approved insecticides if severe"]
        }
    },

    # ---------------------------------------------
    # 21. JOWAR (SORGHUM)
    # ---------------------------------------------
    "jowar": {
        "shoot_fly": {
            "preventive": ["Early sowing", "Seed treatment"],
            "corrective": ["Use recommended insecticides if severe"]
        }
    },

    # ---------------------------------------------
    # 22. SUGARCANE
    # ---------------------------------------------
    "sugarcane": {
        "borer": {
            "preventive": ["Destroy crop residues", "Use resistant varieties"],
            "corrective": ["Release Trichogramma", "Use systemic insecticides"]
        }
    },

    # ---------------------------------------------
    # 23. COTTON
    # ---------------------------------------------
    "cotton": {
        "whitefly": {
            "preventive": ["Remove alternate hosts", "Use reflective mulch"],
            "corrective": ["Neem oil", "Use recommended insecticides if severe"]
        }
    },

    # ---------------------------------------------
    # 24. GROUNDNUT
    # ---------------------------------------------
    "groundnut": {
        "leaf_spot": {
            "preventive": ["Crop rotation", "Use resistant varieties"],
            "corrective": ["Fungicide spray", "Bio-control agents"]
        }
    },

    # ---------------------------------------------
    # 25. SUNFLOWER
    # ---------------------------------------------
    "sunflower": {
        "stem_borer": {
            "preventive": ["Timely sowing", "Destroy stubbles"],
            "corrective": ["Use light traps", "Recommended insecticide"]
        }
    },

    # ---------------------------------------------
    # 26. SOYBEAN
    # ---------------------------------------------
    "soybean": {
        "rust": {
            "preventive": ["Early sowing", "Use resistant varieties"],
            "corrective": ["Apply mancozeb", "Improve airflow"]
        }
    },

    # ---------------------------------------------
    # 27. RED GRAM (TOOR)
    # ---------------------------------------------
    "red gram": {
        "pod_borer": {
            "preventive": ["Use pheromone traps", "Intercropping"],
            "corrective": ["Use Helicoverpa NPV", "Selective insecticide"]
        }
    },

    # ---------------------------------------------
    # 28. GREEN GRAM
    # ---------------------------------------------
    "green gram": {
        "whitefly": {
            "preventive": ["Remove weeds", "Use yellow traps"],
            "corrective": ["Neem oil", "Recommended insecticides"]
        }
    },

    # ---------------------------------------------
    # 29. BLACK GRAM
    # ---------------------------------------------
    "black gram": {
        "leaf_crinkle": {
            "preventive": ["Vector control", "Use certified seeds"],
            "corrective": ["Remove infected plants"]
        }
    },

    # ---------------------------------------------
    # 30. HORSE GRAM
    # ---------------------------------------------
    "horse gram": {
        "leaf_spot": {
            "preventive": ["Proper spacing", "Avoid monocropping"],
            "corrective": ["Fungicide spray"]
        }
    },

    # ---------------------------------------------
    # 31. SESAME
    # ---------------------------------------------
    "sesame": {
        "powdery_mildew": {
            "preventive": ["Use resistant variety", "Avoid high humidity"],
            "corrective": ["Sulfur spray"]
        }
    },

    # ---------------------------------------------
    # 32. CASTOR
    # ---------------------------------------------
    "castor": {
        "semilooper": {
            "preventive": ["Hand-picking larvae", "Light traps"],
            "corrective": ["Neem oil", "Biocontrol agents"]
        }
    },

    # ---------------------------------------------
    # 33. WATERMELON
    # ---------------------------------------------
    "watermelon": {
        "fruit_fly": {
            "preventive": ["Use pheromone traps", "Clean cultivation"],
            "corrective": ["Bait traps", "Recommended insecticide"]
        }
    },

    # ---------------------------------------------
    # 34. PUMPKIN
    # ---------------------------------------------
    "pumpkin": {
        "red_pumpkin_beetle": {
            "preventive": ["Early sowing", "Clean cultivation"],
            "corrective": ["Neem spray", "Recommended insecticide"]
        }
    },

    # ---------------------------------------------
    # 35. BEANS
    # ---------------------------------------------
    "beans": {
        "bean_mosaic_virus": {
            "preventive": ["Use virus-free seeds", "Control aphids"],
            "corrective": ["Remove infected plants"]
        }
    }
}

DEFAULT_PREVENTIVE = ["Scout fields daily", "Maintain hygiene", "Use IPM"]
DEFAULT_CORRECTIVE = ["Consult extension officer", "Use approved inputs only"]

# -------------------------
# Models / ML loader (optional)
# -------------------------
ML_MODEL = None
if ML_MODEL_PATH and joblib:
    try:
        ML_MODEL = joblib.load(ML_MODEL_PATH)
        print("Loaded ML model from", ML_MODEL_PATH)
    except Exception as e:
        print("Could not load model:", e)
        ML_MODEL = None


# -------------------------
# Utility helpers
# -------------------------
def now_ts_ms() -> int:
    return int(time.time() * 1000)


def parse_iso_date(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    try:
        return datetime.fromtimestamp(int(s))
    except Exception:
        return None
    
def translate_to_kannada(key: str) -> str:
    return KANANDA_TRANSLATIONS.get(key, key)


def normalize_text(s: Optional[str]) -> str:
    return (s or "").strip().lower()

def match_synonym(pest_text: str) -> Optional[str]:
    """
    Try to match a reported pest string to canonical pest keys using synonyms.
    Returns canonical pest key (like 'thrips') or None.
    """
    if not pest_text:
        return None
    p = normalize_text(pest_text)
    for canon, syns in PEST_SYNONYMS.items():
        for token in syns:
            if token.lower() in p:
                return canon
    # direct equality fallback
    if p in PEST_SYNONYMS:
        return p
    return None

# -------------------------
# Weather integration
# -------------------------
def fetch_weather_for_district(district: str) -> Optional[Dict[str, Any]]:
    """
    Fetch recent / current weather for district using WEATHER_API_URL.
    The expected provider should accept lat & lon query params; this function is written
    generically for Open-Meteo-like APIs. If your provider differs, adapt accordingly.
    """
    coords = DISTRICT_COORDS.get(district.lower())
    if not coords or not WEATHER_API_URL:
        return None

    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current_weather": True,
        # optionally daily rainfall/humidity forecasts if provider supports
        # (For Open-Meteo you'd request hourly variables)
    }
    if WEATHER_API_KEY:
        # if provider expects key as 'apikey' or 'key', you may need to change param name
        params["apikey"] = WEATHER_API_KEY

    try:
        resp = requests.get(WEATHER_API_URL, params=params, timeout=10)
        if resp.status_code != 200:
            return None
        return resp.json()
    except Exception:
        return None
    
def assess_weather_risk(weather_json: Dict[str, Any]) -> Dict[str, float]:
    """
    Return adjustments to risk score based on weather.
    Simple heuristic:
      - high humidity or recent heavy rainfall increases fungal disease risk -> +0.15
      - high temperature + dryness increases thrips/aphid risk -> +0.10
    The structure of weather_json depends on provider; this checks common keys.
    """
    add_score = 0.0
    reasons = []

    # Try common patterns
    cw = weather_json.get("current_weather") or weather_json.get("current") or {}
    # many APIs use 'temperature' or 'temp', humidity may be absent
    temp = cw.get("temperature") or cw.get("temp") or None
    humidity = None
    # Some APIs return hourly/daily arrays — we try to read 'relativehumidity_2m' if present
    if "hourly" in weather_json and "relativehumidity_2m" in weather_json["hourly"]:
        # pick latest
        try:
            humidity = weather_json["hourly"]["relativehumidity_2m"][-1]
        except Exception:
            humidity = None
    else:
        humidity = cw.get("relativehumidity") or cw.get("humidity")

    # Rainfall: try daily precipitation sum
    rain = None
    if "daily" in weather_json and "rain_sum" in weather_json["daily"]:
        try:
            rain = weather_json["daily"]["rain_sum"][-1]
        except Exception:
            rain = None
    else:
        # provider-specific
        rain = cw.get("precipitation") or cw.get("rain")

    # Heuristics
    if humidity and float(humidity) >= 80:
        add_score += 0.15
        reasons.append(f"High humidity ({humidity}%) increases fungal risk")
    if rain and float(rain) >= 15:
        add_score += 0.10
        reasons.append(f"Recent heavy rain ({rain} mm) favors disease spread")
    if temp and float(temp) >= 33 and (not humidity or float(humidity) < 50):
        add_score += 0.08
        reasons.append(f"High temperature ({temp}°C) with low humidity favors some pests")

    return {"delta": add_score, "reasons": reasons}

# -------------------------
# Firebase helpers
# -------------------------
def read_user(uid: str) -> Optional[Dict[str, Any]]:
    """
    Read user data from Firebase under Users/<uid>
    """
    try:
        ref = db.reference(f"Users/{uid}")
        return ref.get()
    except Exception as e:
        print("Firebase read error:", e)
        return None



def store_alert(uid: str, alert: Dict[str, Any]) -> str:
    ref = db.reference(f"alerts/{uid}")
    aid = f"alert_{now_ts_ms()}"
    ref.child(aid).set(alert)
    return aid



def send_fcm(fcm_token: str, title: str, body: str):
    if not fcm_token:
        return
    try:
        msg = messaging.Message(notification=messaging.Notification(title=title, body=body), token=fcm_token)
        messaging.send(msg)
    except Exception as e:
        # don't fail whole operation on push error; log it
        print("FCM send error:", e)
# -------------------------
# Risk computation (rule + ML + synonyms + weather)
# -------------------------
def compute_rule_score(crop_name: str, logs: Dict[str, Any], district_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Rule-based scoring:
      - farmer symptoms: +0.25 each unique symptom (capped)
      - matching official report for same crop: +0.45 per report (cap)
      - no recent irrigation >10 days: +0.05
      - soil imbalance small +0.05
    Returns dict with score (0..1), triggered pests list, reasons
    """
    score = 0.0
    reasons = []
    triggered = []

    crop_low = normalize_text(crop_name)

    # farmer symptoms
    symptom_count = 0
    for lid, entry in (logs.items() if isinstance(logs, dict) else []):
        if isinstance(entry, dict):
            sym = entry.get("symptoms")
            if sym and normalize_text(sym) not in ("na", "no", "none", ""):
                symptom_count += 1
                score += 0.25
                reasons.append(f"Farmer-reported symptom: {sym}")
    # official reports matching crop or synonyms
    for rep in district_reports:
        rep_crop = normalize_text(rep.get("crop", ""))
        rep_pest_text = rep.get("pest") or ""
        rep_pest = match_synonym(rep_pest_text) or normalize_text(rep_pest_text)
        # match crop name exactly or loosely
        if rep_crop == crop_low or rep_pest in (CROP_DB.get(crop_low, {}) or {}):
            score += 0.45 * float(rep.get("confidence", 1.0))
            reasons.append(f"Official report: {rep.get('pest')} on {rep.get('crop')}")
            triggered.append(rep_pest)

    # irrigation gap heuristic
    # look for lastIrrigationDate in logs
    last_ir = None
    for lid, entry in (logs.items() if isinstance(logs, dict) else []):
        if isinstance(entry, dict) and entry.get("lastIrrigationDate"):
            last_ir = parse_iso_date(entry.get("lastIrrigationDate"))
    if last_ir:
        days = (datetime.utcnow() - last_ir).days
        if days > 10:
            score += 0.05
            reasons.append(f"Last irrigation {days} days ago")

    # soil test heuristic
    for lid, entry in (logs.items() if isinstance(logs, dict) else []):
        if isinstance(entry, dict) and entry.get("soilTest"):
            soil = entry.get("soilTest") or {}
            if soil.get("N", 999) < 10 or soil.get("K", 999) < 5:
                score += 0.05
                reasons.append("Soil test shows low nutrients")

    # cap
    score = min(score, 1.0)
    return {"score": round(score, 3), "reasons": reasons, "triggered": triggered, "symptom_count": symptom_count}
def compute_ml_score(features: Dict[str, float]) -> Optional[float]:
    """
    If ML_MODEL loaded, predict probability. Expects feature dict with known keys by model.
    If no model, returns None.
    """
    if not ML_MODEL:
        return None
    try:
        # This assumes model expects a consistent feature order; define it here
        feat_order = ["nearby_reports", "symptom_count", "days_since_irrigation", "soil_stress", "weather_fungal_delta"]
        x = [features.get(k, 0.0) for k in feat_order]
        prob = float(ML_MODEL.predict_proba([x])[0][1])
        return prob
    except Exception as e:
        print("ML predict error:", e)
        return None
    
def fuse_scores(rule_score: float, ml_score: Optional[float]) -> float:
    """
    Fuse ML and rule scores. If ML exists, weight both:
     - final = 0.6*rule + 0.4*ml (adjustable). If ml missing, return rule.
    """
    if ml_score is None:
        return rule_score
    return round(min(1.0, 0.6 * rule_score + 0.4 * ml_score), 3)


def classify_severity(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.35:
        return "moderate"
    return "low"

def classify_complexity(score: float, symptom_count: int, official_reports: int) -> str:
    # simple rules as requested
    if score < 0.3 and symptom_count <= 1 and official_reports == 0:
        return "simple"
    if 0.3 <= score < 0.6 and (symptom_count > 1 or official_reports > 0):
        return "moderate"
    if 0.6 <= score < 0.8 and official_reports > 0 and symptom_count > 1:
        return "complex"
    if score >= 0.8 and official_reports > 0 and symptom_count > 1:
        return "critical"
    return "moderate"

# -------------------------
# Endpoints
# -------------------------
@app.post("/ingest/report")
def ingest_report(report: PestReport):
    pr_ref = db.reference("pest_reports")
    payload = {
        "district": report.district,
        "crop": report.crop,
        "pest": report.pest,
        "symptoms": report.symptoms,
        "reportDate": report.reportDate or datetime.utcnow().strftime("%Y-%m-%d"),
        "confidence": report.confidence,
        "timestamp": now_ts_ms()
    }
    pr_ref.child(report.reportId).set(payload)
    return {"status": "ok", "reportId": report.reportId}

@app.post("/scan/farmer/{uid}")
def scan_farmer(uid: str, send_push: bool = True, lang: str = "en"):
    """
    Run full scan for a farmer:
      - reads farmActivityLogs (primary + secondary)
      - fetches official reports for district
      - fetches weather and adjusts risk
      - optionally uses ML model if provided
      - stores alerts under /alerts/<uid>/<alertId>
      - optionally sends FCM push (if fcmToken stored)
    """
    user = read_user(uid)
    if not user:
        raise HTTPException(status_code=404, detail="Farmer not found")

    district = (user.get("farmDetails") or {}).get("district")
    if not district:
        raise HTTPException(status_code=400, detail="Farmer district missing")

    farm_logs = user.get("farmActivityLogs", {}) or {}
    fcm_token = user.get("fcmToken")
    district_reports = []
    try:
        # read official reports from firebase
        pr_ref = db.reference("pest_reports")
        all_reports = pr_ref.get() or {}
        cutoff = datetime.utcnow() - timedelta(days=LOOKBACK_DAYS)
        for rid, r in all_reports.items():
            rdate = parse_iso_date(r.get("reportDate"))
            if rdate and rdate >= cutoff and normalize_text(r.get("district", "")) == normalize_text(district):
                district_reports.append(r)
    except Exception as e:
        print("Error loading pest_reports:", e)
        district_reports = []

    # Weather fetch + assessment
    weather_json = fetch_weather_for_district(district)
    weather_assessment = {"delta": 0.0, "reasons": []}
    if weather_json:
        try:
            weather_assessment = assess_weather_risk(weather_json)
        except Exception:
            weather_assessment = {"delta": 0.0, "reasons": []}

    alerts_created = []

    for crop_key, logs in farm_logs.items():
        # determine cropName
        crop_name = None
        if isinstance(logs, dict):
            # logs normally has nested entries; try to find cropName
            for k, v in logs.items():
                if isinstance(v, dict) and v.get("cropName"):
                    crop_name = v.get("cropName")
                    break
            # if top-level mapping had cropName (rare), use it
            if not crop_name and logs.get("cropName"):
                crop_name = logs.get("cropName")
        if not crop_name:
            continue

        # RULE SCORE
        rule_res = compute_rule_score(crop_name, logs, district_reports)
        rule_score = rule_res["score"]

        # weather adjustment
        rule_score = min(1.0, round(rule_score + weather_assessment.get("delta", 0.0), 3))

        # ML features extraction
        days_since_irrig = 0
        last_ir = None
        for lid, entry in (logs.items() if isinstance(logs, dict) else []):
            if isinstance(entry, dict) and entry.get("lastIrrigationDate"):
                last_ir = parse_iso_date(entry.get("lastIrrigationDate"))
        if last_ir:
            days_since_irrig = (datetime.utcnow() - last_ir).days

        soil_stress = 0.0
        for lid, entry in (logs.items() if isinstance(logs, dict) else []):
            if isinstance(entry, dict) and entry.get("soilTest"):
                soil = entry.get("soilTest")
                if soil:
                    if soil.get("N", 999) < 10 or soil.get("K", 999) < 5:
                        soil_stress = 1.0

        features = {
            "nearby_reports": float(len(district_reports)),
            "symptom_count": float(rule_res.get("symptom_count", 0)),
            "days_since_irrigation": float(days_since_irrig),
            "soil_stress": float(soil_stress),
            "weather_fungal_delta": float(weather_assessment.get("delta", 0.0))
        }

        ml_prob = compute_ml_score(features)

        final_score = fuse_scores(rule_score, ml_prob)
        severity = classify_severity(final_score)
        complexity = classify_complexity(final_score, rule_res.get("symptom_count", 0), len(district_reports))

        # select triggered pest (prefer official, else try logs)
        triggered = rule_res.get("triggered") or []
        trigger_pest = None
        if triggered:
            trigger_pest = triggered[0]
        else:
            # attempt to read pest names in farmer logs
            for lid, entry in (logs.items() if isinstance(logs, dict) else []):
                if isinstance(entry, dict) and entry.get("pestDiseaseName"):
                    m = match_synonym(entry.get("pestDiseaseName"))
                    if m:
                        trigger_pest = m
                        break

        # measures
        preventive = DEFAULT_PREVENTIVE
        corrective = DEFAULT_CORRECTIVE
        if trigger_pest and crop_name.lower() in CROP_DB and trigger_pest in CROP_DB[crop_name.lower()]:
            pest_info = CROP_DB[crop_name.lower()][trigger_pest]
            preventive = pest_info.get("preventive", preventive)
            corrective = pest_info.get("corrective", corrective)
        else:
            # if no exact pest, but crop has entries, pick top measures
            if crop_name.lower() in CROP_DB:
                # grab first pest's measures
                for pkey, pval in CROP_DB[crop_name.lower()].items():
                    preventive = pval.get("preventive", preventive)
                    corrective = pval.get("corrective", corrective)
                    break

        alert = {
            "uid": uid,
            "cropKey": crop_key,
            "cropName": crop_name,
            "timestamp": now_ts_ms(),
            "riskScore": final_score,
            "severity": severity,
            "complexityLevel": complexity,
            "triggerPest": trigger_pest or "unknown",
            "reasons": rule_res.get("reasons", []) + weather_assessment.get("reasons", []),
            "symptomCount": rule_res.get("symptom_count", 0),
            "officialReports": len(district_reports),
            "preventiveMeasures": preventive,
            "correctiveMeasures": corrective,
            "mlProbability": ml_prob,
            "weatherDelta": weather_assessment.get("delta", 0.0)
        }

        aid = store_alert(uid, alert)
        alerts_created.append({**alert, "alertId": aid})

        # push notification
        if send_push and fcm_token:
            title = f"Pest Alert: {crop_name} ({severity})"
            body = f"Risk {round(final_score*100)}% • Complexity: {complexity}"
            try:
                send_fcm(fcm_token, title, body)
            except Exception as e:
                print("Push error:", e)

    return {"status": "ok", "created": alerts_created}

@app.get("/alerts/{uid}")
def get_alerts(uid: str, lang: str = "en"):
    raw = db.reference(f"alerts/{uid}").get() or {}
    if lang and lang.lower().startswith("kn"):
        # translate top-level fields where mapping exists
        translated = {}
        for aid, a in raw.items():
            t = {}
            for k, v in a.items():
                key_trans = translate_to_kannada(k) if isinstance(k, str) else k
                # for enumerations like severity/complexity translate values too
                if k in ("severity", "complexityLevel"):
                    if isinstance(v, str):
                        val_trans = translate_to_kannada(v)
                        t[key_trans] = val_trans
                    else:
                        t[key_trans] = v
                else:
                    t[key_trans] = v
            translated[aid] = t
        return translated
    return raw

@app.get("/health")
def health():

    return {"status": "ok", "time": datetime.utcnow().isoformat()}
