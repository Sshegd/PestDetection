from translator import translate_to_kannada

class PestEngine:

    def analyse(self, crops, district, soil, lang="en"):
        results = []

        for crop in crops:
            crop_l = crop.lower()

            hist = PEST_HISTORY.get(district.lower(), {}).get(crop_l, {})
            db = PEST_DB.get(crop_l, {})

            for pest, meta in db.items():

                risk = hist.get(pest, {}).get("risk_level", "LOW")

                if soil.lower() in meta.get("soil", []):

                    symptoms = meta["symptoms"]
                    preventive = meta["preventive"]
                    treatment = meta["corrective"]

                    # 🌐 AUTO TRANSLATE
                    if lang == "kn":
                        symptoms = translate_to_kannada(symptoms)
                        preventive = translate_to_kannada(preventive)
                        treatment = translate_to_kannada(treatment)

                    results.append({
                        "crop": crop,
                        "pest": pest,
                        "risk": risk,
                        "symptoms": symptoms,
                        "preventive": preventive,
                        "treatment": treatment
                    })

        return results
