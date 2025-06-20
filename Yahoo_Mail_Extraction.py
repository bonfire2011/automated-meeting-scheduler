import imaplib
import email
import pandas as pd
from datetime import datetime, timezone, timedelta
import os


YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
TODAY = datetime.now().strftime("%d-%b-%Y")
FILENAME = f"yahoo_emails_received_on_{YESTERDAY}.csv"

ALL_EMAIL_PATH = "yahoo_emails_all.csv"



#Should work with emails except for those sent by Yahoo <no-reply@cc.yahoo.com>
def remove_formula_related_texts(text):
    if isinstance(text, str) and text.startswith('='):
        return "'" + text
    return text

EMAIL = ''

#one time passoword
ONE_TIME_PASSWORD = ''


mail = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
mail.login(EMAIL, ONE_TIME_PASSWORD)
mail.select(mailbox="INBOX")

#status, messages = mail.search(None, "ALL")
status, messages = mail.search(None, f'(SINCE "{YESTERDAY}" BEFORE "{TODAY}")')

email_ids = messages[0].split()




data = []

for num in email_ids:
    status, message_data = mail.fetch(num, "(RFC822)")

    message = email.message_from_bytes(message_data[0][1])

    subject = message["subject"]
    sender = message["from"]
    date = message["date"]
    body = ""

    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                payload = part.get_payload(decode = True)

                if payload:
                    body = payload.decode(errors='replace')
                break

            else:
                payload = message.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors= 'replace')
            
    data.append({"From":sender, "Subject": subject, "Date": date, "Body": body})

for row in data:
    row["Subject"] = remove_formula_related_texts(row["Subject"])
    row["Body"] = remove_formula_related_texts(row["Body"])
df_new = pd.DataFrame(data)
df_new["Date_parsed"] = pd.to_datetime(df_new["Date"], errors = 'coerce', utc = True)
df_new["Date_only"] = df_new["Date_parsed"].dt.date

df_new.to_csv(FILENAME, index=False, encoding="utf-8")




if os.path.exists(ALL_EMAIL_PATH):
    df_all_emails = pd.read_csv(ALL_EMAIL_PATH)
    df_combined = pd.concat([df_all_emails, df_new], ignore_index=True)
    df_combined.drop_duplicates(subset=["From", "Subject", "Date"], inplace=True)
    df_combined.to_csv(ALL_EMAIL_PATH, index= False, encoding="utf-8")
