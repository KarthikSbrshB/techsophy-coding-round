import pandas as pd
from core.risk_finder import predict_risk
from core.screening_rules import get_screening_interval
from core.scheduler import calculate_next_screening
from datetime import datetime

df = pd.read_csv("data/test_patient_data.csv")

cancer_types = {
    "breast": "last_breast_screen",
    "cervical": "last_cervical_screen",
    "colorectal": "last_colorectal_screen"
}

print("\n🩺 Cancer Screening Reminders\n")

for _, row in df.iterrows():
    risk_result = predict_risk(row)

    print(f"\n👤 {row['name']}")
    
    for cancer, last_screen_col in cancer_types.items():
        if row["gender"] == "M" and cancer in ["breast", "cervical"]:
            continue

        risk_level = risk_result.get(cancer, "Unknown")
        interval = get_screening_interval(risk_level, cancer)
        last_screen_date = row.get(last_screen_col, "")
        next_due = calculate_next_screening(last_screen_date, interval)

        try:
            due_date = datetime.strptime(str(next_due), "%Y-%m-%d").date()
            today = datetime.today().date()
            days_left = (due_date - today).days
        except Exception:
            due_date = None
            days_left = None

        needs_reminder = False
        if risk_level.lower() == "high":
            needs_reminder = True
        elif risk_level.lower() == "medium" and days_left is not None and days_left <= 7:
            needs_reminder = True
        elif risk_level.lower() == "low" and days_left is not None and days_left <= 0:
            needs_reminder = True

        reason = ""
        if needs_reminder:
            if days_left is not None and days_left < 0:
                reason = f"(⚠️ Overdue by {abs(days_left)} days)"
            elif days_left == 0:
                reason = "(Due Today!)"
            elif days_left is not None:
                reason = f"(Due in {days_left} days)"

        print(f"  • {cancer.capitalize()} Cancer (Risk: {risk_level}) → Next: {next_due} {reason} {'🔔 Reminder!' if needs_reminder else ''}")