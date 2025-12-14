from firebase_reader import get_farmer_context
from firebase_admin import db
from models import PestAlert
from gemini_helper import translate_to_kannada

class PestEngine:

    def run_scan(self, uid: str, lang: str):

        context = get_farmer_context(uid)

        district = context["district"]
        soil = context["soilType"]
        crops = context["crops"]

        alerts = []

        for crop in crops:
            alerts.append(
                PestAlert(
                    cropName=crop,
                    pestName="Brown Planthopper",
                    riskLevel="High",
                    symptoms=[
                        "Yellowing of leaves",
                        "Hopper burn patches"
                    ],
                    preventive=[
                        "Avoid excess nitrogen fertilizer"
                    ],
                    corrective=[
                        "Spray Imidacloprid as recommended"
                    ]
                )
            )

        if lang == "kn":
            for a in alerts:
                a.pestName = translate_to_kannada(a.pestName)
                a.symptoms = [translate_to_kannada(s) for s in a.symptoms]
                a.preventive = [translate_to_kannada(p) for p in a.preventive]
                a.corrective = [translate_to_kannada(c) for c in a.corrective]

        db.reference(f"alerts/{uid}").set({
            "alerts": [a.dict() for a in alerts]
        })
