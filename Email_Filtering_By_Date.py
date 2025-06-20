from datetime import datetime

def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_yes_no(prompt):
    while True:
        yes_no = (input(prompt)).lower()

        if yes_no in ["yes", "y", "no", "n"]:
            return yes_no
        else:
            print("Please enter yes, y, no, or n.")

def filter_emails_by_date(df):
    y_n = get_yes_no("Do you want to specify the dates you want to retrieve emails between? Press y/n. ")
    print("You said:", y_n)
    if y_n in ["no", "n"]:
        return df
    start_date = get_valid_date("Specify the start date to retrieve emails from (YYYY-MM-DD): ")
    end_date = get_valid_date("Specify the end date to retrieve emails until (YYYY-MM-DD): ")
    print("Start date:", start_date)
    print("End date:", end_date)

    return df[(df["Date_only"] >= start_date) & (df["Date_only"] <= end_date)]



