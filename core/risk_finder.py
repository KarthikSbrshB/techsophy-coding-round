def calculate_risk(patient):
    score = 0

    if patient['age'] >= 50:
        score += 1

    if str(patient['smoking']).lower() == 'true':
        score += 1

    if str(patient['family_history']).lower() == 'true':
        score += 2
        
    print(f"{patient['name']} → Score: {score}")

    if score >= 3:
        return "High"
    elif score == 2:
        return "Medium"
    else:
        return "Low"