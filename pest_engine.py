from firebase_admin import db
from gemini_helper import translate_to_kannada
from models import PestAlert

class PestEngine:

    def run_scan(self, uid: str, district: str, soil: str, lang: str):

        # Example static logic (replace with your real DB logic)
        alerts = [
            PestAlert(
                cropName="paddy",
                pestName="Brown Planthopper",
                riskLevel="High",
                symptoms=[
                    "Yellowing of leaves",
                    "Hopper burn patches"
                ],
                preventive=[
                    "Avoid excess nitrogen fertilizer",
                    "Maintain proper spacing"
                ],
                corrective=[
                    "Spray Imidacloprid",
                    "Use recommended dosage"
                ]
            )
        ]

        # Translate if Kannada
        if lang == "kn":
            for a in alerts:
                a.pestName = translate_to_kannada(a.pestName)
                a.symptoms = [translate_to_kannada(s) for s in a.symptoms]
                a.preventive = [translate_to_kannada(p) for p in a.preventive]
                a.corrective = [translate_to_kannada(c) for c in a.corrective]

        # Store in Firebase
        db.reference(f"alerts/{uid}").set({
            "alerts": [a.dict() for a in alerts]
        })
