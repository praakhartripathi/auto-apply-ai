import csv
import os
import gspread
from datetime import datetime

class Tracker:
    def __init__(self, sheet_name="Auto-Apply Jobs Tracker", csv_fallback="applied_jobs.csv"):
        self.sheet_name = sheet_name
        self.csv_fallback = csv_fallback
        self.client = None
        self.sheet = None
        
        try:
            # Assumes the user placed 'service_account.json' in the root directory
            if os.path.exists("service_account.json"):
                self.client = gspread.service_account(filename="service_account.json")
                try:
                    self.sheet = self.client.open(self.sheet_name).sheet1
                    print(f"Connected to Google Sheet: '{self.sheet_name}'")
                except gspread.exceptions.SpreadsheetNotFound:
                    print(f"Could not find Sheet '{self.sheet_name}'. Ensure you shared the sheet with your service account email.")
            else:
                print("No 'service_account.json' found. Falling back to CSV tracking only.")
        except Exception as e:
            print(f"Google Sheets init error: {e}")
            
        # Init CSV backup if needed
        if not os.path.exists(self.csv_fallback):
            with open(self.csv_fallback, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Time", "Job Title", "Company"])
                
    def log_application(self, job_title, company):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # Log to Google Sheet
        if self.sheet:
            try:
                self.sheet.append_row([date_str, time_str, job_title, company])
                print("📝 Logged application to Google Sheet.")
            except Exception as e:
                print(f"Failed to append to Google Sheet: {e}.")
        
        # Always log to CSV as backup
        try:
            with open(self.csv_fallback, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([date_str, time_str, job_title, company])
        except Exception as e:
            print(f"Failed to write to CSV logs: {e}")
