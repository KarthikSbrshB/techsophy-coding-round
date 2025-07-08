def get_screening_interval(risk_level: str, cancer_type: str) -> int:
    rules = {
        "breast": {
            "Low": 24,
            "Medium": 12,
            "High": 6
        },
        "cervical": {
            "Low": 36,
            "Medium": 24,
            "High": 12
        },
        "colorectal": {
            "Low": 60,
            "Medium": 36,
            "High": 24
        }
    }

    return rules.get(cancer_type, {}).get(risk_level, None)