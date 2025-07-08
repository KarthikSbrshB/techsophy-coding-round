from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def calculate_next_screening(last_date_str, interval_months: int) -> str:
    if pd.isna(last_date_str) or str(last_date_str).strip() == "":
        return "Due Now"

    try:
        last_date = datetime.strptime(str(last_date_str).strip(), "%Y-%m-%d")
        next_date = last_date + relativedelta(months=interval_months)
        return next_date.strftime("%Y-%m-%d")
    except Exception:
        return "Due Now"