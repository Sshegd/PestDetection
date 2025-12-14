from firebase_admin import db

def get_farmer_context(uid: str):

    user_ref = db.reference(f"Users/{uid}")
    user_data = user_ref.get()

    if not user_data:
        raise ValueError("User not found")

    # ✅ DIRECT FIELDS (NO profile)
    district = user_data.get("district")
    soil_type = user_data.get("soilType")

    if not district or not soil_type:
        raise ValueError("District or soilType missing in user data")

    # ✅ CROPS FROM FARM ACTIVITY LOGS
    farm_logs = user_data.get("farmActivityLogs", {})

    crops = []

    # Primary crop
    primary = farm_logs.get("primary_crop", {})
    for _, entry in primary.items():
        name = entry.get("cropName")
        if name:
            crops.append(name.lower())
            break

    # Secondary crops
    secondary = farm_logs.get("secondary_crop", {})
    for _, entry in secondary.items():
        name = entry.get("cropName")
        if name:
            crops.append(name.lower())

    if not crops:
        raise ValueError("No crops found for user")

    return {
        "district": district,
        "soilType": soil_type,
        "crops": list(set(crops))
    }
