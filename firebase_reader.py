from firebase_admin import db
import json

def get_farmer_context(uid: str):

    ref = db.reference(f"Users/{uid}")
    user = ref.get()

    if not user:
        raise ValueError("User node not found")

    # 🔥 DEBUG: PRINT FULL USER NODE
    print("🔥 USER DATA:", json.dumps(user, indent=2))

    district = user.get("district")
    soil = user.get("soilType")

    if not district or not soil:
        raise ValueError(
            f"District or soilType missing. Found district={district}, soilType={soil}"
        )

    logs = user.get("farmActivityLogs", {})
    crops = []

    for section in ["primary_crop", "secondary_crop"]:
        for _, v in logs.get(section, {}).items():
            name = v.get("cropName")
            if name:
                crops.append(name.lower())

    if not crops:
        raise ValueError("No crops found in farmActivityLogs")

    return {
        "district": district,
        "soilType": soil,
        "crops": list(set(crops))
    }
