# automated-meeting-scheduler
Automatically schedules meetings based on email absence notifications using GPT-4 and Google Calendar API.


---

### 1. How It Works

**STEP 1 — Email Extraction**  
`yahoo_mail_extraction.py`:  
Fetches all Yahoo emails sent the day before (recommended to run once daily).  
Extracted emails are saved as a CSV file.

**STEP 2 — Email Classification with GPT-4.1**  
`GPT_4_1_email_automation.py`:  
Processes the emails fetched in Step 1 using GPT-4.1.  
Classifies whether the sender is notifying absence, and if so, extracts absence dates.  
Stores results in a CSV (`ABSENT_CSV_Format`) showing who is absent and when.

**STEP 3 — Calendar Scheduling**  
`google_calendar_automation.py`:  
Creates 45-minute "Check-in" events on available weekdays, avoiding dates when attendees are absent.  
Meetings are scheduled using the Google Calendar API via OAuth 2.0.

---

### 2. Requirements
- **Yahoo Mail account**
- **OpenAI API Key + Credits**
- **Google Calendar OAuth 2.0 credentials**

---

### 3. Values You Must Assign

```python
EMAIL = "your_yahoo_email@example.com"
ONE_TIME_PASSWORD = "your_yahoo_app_password"

client = OpenAI(api_key="your_openai_api_key")
flow = InstalledAppFlow.from_client_secrets_file("your_google_oauth_credentials.json", SCOPES)
```

### 4. Values You Can Customize
```python
ALL_EMAIL_PATH = "your_combined_email_log.csv"  # You can change the filename
```
### 5. Additional Configurable Options

Meeting Settings (in google_calendar_automation.py)
Customize the meeting title, duration, start time, and time zone:

```python
'summary': 'Your Meeting Title',
start_dt = dt.replace(hour=9, minute=0)
end_dt = dt.replace(hour=10, minute=0)
'timeZone': 'Your/Preferred_Timezone'
```

Email Filtering Logic
Use Email_Filtering_By_Date.py to control which emails are fetched —
for example, you can change the date range (e.g., fetch emails from a specific day or range) or choose to fetch all emails regardless of date.

GPT-4.1 Prompts (in GPT_4_1_email_automation.py)
Adjust the system and user prompts used for classifying emails and extracting absence dates.
You can fine-tune these prompts for different languages, tone, or classification criteria.