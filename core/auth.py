import os
from playwright.sync_api import Playwright, BrowserContext

STATE_FILE = "config/state.json"

def get_browser_context(playwright: Playwright, headless: bool = False) -> BrowserContext:
    browser = playwright.chromium.launch(headless=headless)
    
    # Use existing state if available
    context = None
    if os.path.exists(STATE_FILE):
        try:
            context = browser.new_context(storage_state=STATE_FILE)
            print("Loaded existing browser session state.")
        except Exception as e:
            print(f"Error loading state: {e}. Starting fresh.")
    
    if not context:
        context = browser.new_context()
        
    return context

def login_linkedin(context: BrowserContext):
    """
    Checks if the user is logged into LinkedIn. 
    If not, it waits for the user to manually log in and saves the state.
    """
    page = context.new_page()
    page.goto("https://www.linkedin.com/feed/")
    
    # Try to find an element indicative of being logged in, e.g., the global nav profile button
    try:
        page.wait_for_selector(".global-nav__me", timeout=5000)
        print("Already logged into LinkedIn.")
    except Exception:
        print("Not logged in to LinkedIn. Redirecting to login page.")
        page.goto("https://www.linkedin.com/login")
        print("*****************************************************************")
        print("Please log in to LinkedIn in the browser window.")
        print("The script will wait until you successfully log in.")
        print("*****************************************************************")
        
        # Wait for the user to log in and the feed to load
        page.wait_for_selector(".global-nav__me", timeout=0) # Wait infinitely until logged in
        print("Login successful! Saving session state...")
        
    context.storage_state(path=STATE_FILE)
    page.close()
    return context
