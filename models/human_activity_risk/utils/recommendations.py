def risk_badge(score):
    if score < 30:
        return "🟢 LOW RISK"
    elif score < 70:
        return "🟡 MODERATE RISK"
    else:
        return "🔴 HIGH RISK"


def recommendation(score):
    """
    Detailed human activity impact recommendations based on activity risk.
    Includes emojis and multiline descriptions (flattened later in main.py).
    """
    if score < 30:
        return (
            "🟢 Low human activity detected.\n"
            "Marine ecosystem appears stable with minimal disturbance.\n"
            "Recommended actions:\n"
            "- Continue periodic monitoring.\n"
            "- Maintain existing environmental practices.\n"
            "- Encourage low-impact tourism."
        )

    elif score < 70:
        return (
            "🟡 Moderate activity detected.\n"
            "There is noticeable pressure on the ecosystem from shipping, tourism,\n"
            "and coastal industries. Recommended actions:\n"
            "- Enforce vessel speed regulations.\n"
            "- Regulate coastal construction activities.\n"
            "- Increase water-quality checks.\n"
            "- Strengthen industrial effluent monitoring."
        )

    else:
        return (
            "🔴 High human activity intensity detected.\n"
            "The region is likely experiencing significant environmental stress\n"
            "due to ports, heavy shipping traffic, tourism clusters, and industries.\n"
            "Immediate recommended actions:\n"
            "- Restrict non-essential ship movements.\n"
            "- Implement emergency pollution-control measures.\n"
            "- Schedule port operations to reduce peak congestion.\n"
            "- Increase inspections of industrial discharge sources.\n"
            "- Deploy rapid-response marine conservation teams."
        )
