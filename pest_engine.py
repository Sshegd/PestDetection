from firebase_reader import get_farmer_context
from firebase_admin import db
from models import PestAlert

class PestEngine:

    def run_scan(self, uid: str, lang: str = "en"):
        ctx = get_farmer_context(uid)

        alerts = []

        for crop in ctx["crops"]:
            alerts.append(
                PestAlert(
                    cropName=crop,
                    pestName="Brown Planthopper",
                    riskLevel="High",
                    symptoms=["Yellowing leaves", "Hopper burn"],
                    preventive=["Avoid excess nitrogen"],
                    corrective=["Spray Imidacloprid"]
                )
            )

        db.reference(f"alerts/{uid}").set({
            "alerts": [a.dict() for a in alerts]
        })
