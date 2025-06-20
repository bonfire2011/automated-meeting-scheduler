from datetime import datetime, timedelta
from GPT_4_1_Email_Classification import ABSENT_CSV
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow



absent_senders_df = pd.read_csv(ABSENT_CSV)
start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
end_date = start_date + timedelta(weeks=1)


all_dates_dt = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]


all_dates_mmdd = [d.strftime("%m/%d") for d in all_dates_dt]


available_dates = {}

for sender, group in absent_senders_df.groupby("Sender"):
    # Parse and normalize absent dates
    absent_mmdd = set(group["Individual_Absent_Date"])
    absent_dates = pd.to_datetime(list(absent_mmdd), format="%m/%d", errors="coerce").dropna()
    absent_dates = pd.to_datetime([d.replace(year=datetime.today().year) for d in absent_dates])
    

    if not absent_dates.empty:
        individual_end_date = max(absent_dates.max(), start_date + timedelta(weeks=1))
    else:
        individual_end_date = start_date + timedelta(weeks=1)


    all_dt = [start_date + timedelta(days=i) for i in range((individual_end_date - start_date).days + 1)]
    all_mmdd = [d.strftime("%m/%d") for d in all_dt]

    # Skip weekends and already-absent dates
    present_days = [
        dt for dt, mmdd in zip(all_dt, all_mmdd)
        if mmdd not in absent_mmdd and mmdd != "Unknown" and dt.weekday() < 5
    ]

    available_dates[sender] = present_days






SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file("", SCOPES)
creds = flow.run_local_server(port=0)
service = build('calendar', 'v3', credentials=creds)


calendar_id = 'primary'



def create_event(email, dt):  # dt is a datetime object
    start_dt = dt.replace(hour=10, minute=0)
    end_dt = dt.replace(hour=10, minute=45)
    event = {
        'summary': 'Project Meeting',
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [{'email': email}],
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()



for sender_email, datetimes in available_dates.items():
    for dt in datetimes:
        create_event(sender_email, dt)
