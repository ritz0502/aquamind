def convert_risk_level(level):
    level = level.lower()
    if "low" in level:
        return 0.2
    if "medium" in level:
        return 0.5
    if "high" in level:
        return 0.9
    return 0.5


def convert_pollution(pred):
    objs = pred.get("detected_objects", [])
    count = len(objs)

    if count == 0:
        return 0.2
    if count <= 2:
        return 0.5
    return 0.9


def calculate_mehi(data):
    R = convert_risk_level(data["risk"]["risk_level"])
    P = convert_pollution(data["pollution"])
    C = data.get("coral", {}).get("health_score", 0.7)

    mehi = 0.4*(1-R) + 0.3*(1-P) + 0.3*(C)
    return round(mehi, 3)
