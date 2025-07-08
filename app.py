import pandas as pd
from core.risk_finder import calculate_risk
from core.screening_rules import get_screening_interval
from core.scheduler import calculate_next_screening
from core.reminder_gen import is_reminder_due

df = pd.read_csv("data/patient_data.csv")

cancer_types = {
    "breast": "last_breast_screen",
    "cervical": "last_cervical_screen",
    "colorectal": "last_colorectal_screen"
}

print("\nCancer Screening Reminders\n")

for _, row in df.iterrows():
    risk = calculate_risk(row)
    print(f"\n{row['name']} (Risk: {risk})")

    for cancer, last_screen_col in cancer_types.items():
        # Skip breast/cervical for males
        if row["gender"] == "M" and cancer in ["breast", "cervical"]:
            continue

        interval = get_screening_interval(risk, cancer)
        last_screen_date = row.get(last_screen_col, "")
        next_due = calculate_next_screening(last_screen_date, interval)
        needs_reminder = is_reminder_due(next_due)

        print(f"  • {cancer.capitalize()} Cancer → Next: {next_due} {'Reminder!' if needs_reminder else ''}")