def risk_badge(score):
    if score < 30:
        return "🟢 LOW RISK"
    elif score < 70:
        return "🟡 MODERATE RISK"
    else:
        return "🔴 HIGH RISK"

def recommendation(score):
    """
    Return smart recommendations to decrease pollution based on risk score.
    These are general, replace with policy-specific text if needed.
    """
    if score < 30:
        return "Maintain current practices; continue monitoring."
    elif score < 70:
        return ("Moderate risk: enforce vessel speed limits, schedule port traffic, "
                "tighten industrial discharge monitoring, and promote sustainable tourism.")
    else:
        return ("High risk: restrict non-essential ship movements, impose temporary port limits, "
                "increase inspections on industrial effluent, and implement emergency response plans.")
