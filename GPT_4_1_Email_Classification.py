import pandas as pd
from openai import OpenAI
from Yahoo_Mail_Extraction import FILENAME, YESTERDAY
from datetime import datetime, timedelta
import re
from Absence_CSV_Format import format_absence_dates
#from filter_emails_by_date import filter_emails_by_date


ABSENT_CSV = f"Absent_On_{YESTERDAY}.csv"


df_emails = pd.read_csv(FILENAME)
df_emails = df_emails.dropna(subset=["Body"])
df_emails = df_emails.reset_index(drop=True)

#Redo the conversion
df_emails["Date_only"] = pd.to_datetime(df_emails["Date_only"], errors='coerce').dt.date
#df_emails = filter_emails_by_date(df_emails)



#Please type in your api key
client = OpenAI(api_key="")

absent_senders = []
prompt1 = "Is the sender notifying the recipient that they will be absent or unavailable (Absent Notice)? Answer only 'Yes' or 'No'."
prompt0 = "Is the sender notifying the recipient that they will be absent or unavailable (e.g., vacation, sick leave, out-of-office)? Answer only 'Yes' or 'No'."

prompt2 = (
        "If the sender mentions a date or date range when they will be absent (e.g., vacation, out-of-office, sick leave), extract that date or range.\n"
        "If the absence is mentioned using relative terms like 'tomorrow' or 'next week', resolve it based on the sent date.\n"
        "If no absence date is given, respond with 'Unknown'.\n\n"
        "Respond with only the date or date range (e.g., '06/05', '06/10~06/15', or 'Unknown')."
        )

prompt3 = (
        "If the sender mentions a date or date range when they will be absent, extract that date or range.\n"
        "If no absence date is given, respond with 'Unknown'.\n"
        "Respond with only the date or date range in the MM/DD format(e.g., '06/05', '06/10~06/15', or 'Unknown')."
        )



for i, row in df_emails.iterrows():
    body = row["Body"]
    sender = row["From"]
    sent_date = row["Date_only"]


    response1 = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": prompt1},
        {"role": "user", "content": body}
        ]
    )

    reply1 = response1.choices[0].message.content.strip()

    if reply1.lower().startswith("yes"):




        user_input = f"This email was sent on {sent_date}:\n\n{body}"


        response2 = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": prompt3},
                {"role": "user", "content": user_input}
            ]
        )
        absence_date = response2.choices[0].message.content.strip()

        absent_senders.append({
            "Sender": sender,
            "Sent": sent_date,
            "Absent_On": absence_date
        })

absent_senders_df = pd.DataFrame(absent_senders)
absent_senders_df["Individual_Absent_Date"] = absent_senders_df.apply(lambda row: format_absence_dates(row["Absent_On"], row["Sent"]), axis=1)
absent_senders_df_formatted = absent_senders_df.explode("Individual_Absent_Date")


pd.DataFrame(absent_senders_df_formatted).to_csv(ABSENT_CSV, index = False)