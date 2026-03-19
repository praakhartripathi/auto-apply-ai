import os
import json
from playwright.sync_api import sync_playwright
from core.auth import get_browser_context, login_linkedin
from core.scraper import process_jobs
from core.bot import auto_apply
from core.optimizer import extract_keywords_from_pdf
from core.tracker import Tracker

def load_settings():
    with open("config/settings.json", "r") as f:
        return json.load(f)

def run_application_bot():
    print("Starting Auto-Apply AI...")
    settings = load_settings()
    
    # Extract keywords from the user's PDF resume
    resume_path = "Prakhar_s_Resume.pdf"
    resume_keywords = extract_keywords_from_pdf(resume_path)
    
    # Initialize the Tracker (Logs to Google Sheets & CSV)
    tracker = Tracker(sheet_name="Auto-Apply Jobs Tracker")
    
    job_title = settings["search_filters"]["job_titles"][0]
    location = settings["search_filters"]["locations"][0]
    limit = settings.get("daily_applications_limit", 30)

    with sync_playwright() as playwright:
        # Launch browser in non-headless mode so user can see and login
        context = get_browser_context(playwright, headless=False)
        
        try:
            # Login if necessary
            login_linkedin(context)
            
            page = context.new_page()
            
            # Start processing
            applied = process_jobs(
                page=page, 
                keyword=job_title, 
                location=location, 
                resume_keywords=resume_keywords, 
                apply_function=auto_apply, 
                limit=limit,
                tracker=tracker
            )
            
            print(f"\nFinished run. Total applied: {applied}")
            page.close()
            
        except Exception as e:
            print(f"A fatal error occurred: {e}")
            
        finally:
            context.close()

if __name__ == "__main__":
    run_application_bot()
