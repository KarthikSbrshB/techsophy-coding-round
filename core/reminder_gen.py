from datetime import datetime, timedelta

def is_reminder_due(next_screen_date_str: str) -> bool:
    if next_screen_date_str == "Due Now":
        return True

    try:
        next_screen_date = datetime.strptime(next_screen_date_str, "%Y-%m-%d")
        today = datetime.today()
        days_until_due = (next_screen_date - today).days

        return days_until_due <= 30
    except Exception:
        return False