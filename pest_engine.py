def run_scan(district, soil, primary, secondary, lang):

    crops = [primary]
    if secondary:
        crops.append(secondary)

    alerts = []

    for crop in crops:
        alerts.append({
            "crop": crop,
            "pest": "Root Grub",
            "risk": "High",
            "symptoms": "Wilting, yellow leaves",
            "preventive": "Proper drainage",
            "treatment": "Chlorpyrifos soil application"
        })

    return alerts
