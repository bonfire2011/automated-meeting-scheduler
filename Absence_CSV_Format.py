import pandas as pd
from datetime import datetime, timedelta
import re


def format_absence_dates(absent_str, sent_date):
    if not isinstance(absent_str, str) or absent_str.strip().lower() == "unknown":
        return ["Unknown"]

    try:
        year = pd.to_datetime(sent_date).year
    except:
        year = datetime.now().year

    text = absent_str.replace("–", "~")
    parts = re.split(r",\s*", text.strip())
    dates = []

    for part in parts:
        part = part.strip()
        if "~" in part:
            try:
                start_str, end_str = part.split("~")
                if "/" not in end_str:

                    start_month = start_str.split("/")[0]
                    end_str = f"{start_month}/{end_str.strip()}"
                start_date = datetime.strptime(f"{year}/{start_str.strip()}", "%Y/%m/%d")
                end_date = datetime.strptime(f"{year}/{end_str.strip()}", "%Y/%m/%d")
                dates.extend([(start_date + timedelta(days=i)).strftime("%m/%d") for i in range((end_date - start_date).days + 1)])
            except:
                continue
        else:
            try:
                date = datetime.strptime(f"{year}/{part.strip()}", "%Y/%m/%d")
                dates.append(date.strftime("%m/%d"))
            except:
                continue

    return dates if dates else ["Unknown"]