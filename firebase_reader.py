from firebase_admin import db

def get_farmer_context(uid: str):
    user = db.reference(f"Users/{uid}").get()

    if not user:
        raise ValueError("User not found")

    # ✅ DIRECT FIELDS (NO profile)
    district = user.get("district")
    soil = user.get("soilType")

    if not district or not soil:
        raise ValueError("District or soilType missing in Users node")

    crops = []

    logs = user.get("farmActivityLogs", {})

    # primary crop
    primary = logs.get("primary_crop", {})
    for _, v in primary.items():
        if "cropName" in v:
            crops.append(v["cropName"].lower())
            break

    # secondary crops
    secondary = logs.get("secondary_crop", {})
    for _, v in secondary.items():
        if "cropName" in v:
            crops.append(v["cropName"].lower())

    if not crops:
        raise ValueError("No crops found in farmActivityLogs")

    return {
        "district": district,
        "soilType": soil,
        "crops": list(set(crops))
    }
