import time

def auto_apply(page):
    """
    Attempts to click the Easy Apply button and complete the application.
    """
    try:
        easy_apply_buttons = page.locator("button:has-text('Easy Apply')").all()
        if not easy_apply_buttons:
            print("No Easy Apply button available for this job.")
            return False
            
        easy_apply_buttons[0].click()
        print("Clicked Easy Apply.")
        
        # Keep clicking 'Next' or 'Review' until 'Submit application' is available
        max_steps = 10
        for _ in range(max_steps):
            time.sleep(2)
            
            # Check for error messages indicating we need manual input
            error_count = page.locator(".artdeco-inline-feedback--error").count()
            if error_count > 0:
                print("Form requires manual input. Skipping or waiting for user...")
                # Alternatively we could wait for user to fix the form
                # return False
                
            submit_btn = page.locator("button:has-text('Submit application')").all()
            if submit_btn:
                submit_btn[0].click()
                print("✅ Successfully submitted Easy Apply application!")
                time.sleep(2)
                
                # Close the success modal
                close_btn = page.locator("button.artdeco-modal__dismiss").all()
                if close_btn:
                    close_btn[0].click()
                return True
                
            next_btn = page.locator("button:has-text('Next')").all()
            if next_btn:
                next_btn[0].click()
                continue
                
            review_btn = page.locator("button:has-text('Review')").all()
            if review_btn:
                review_btn[0].click()
                continue
                
            # If we don't find Next, Review, or Submit, maybe it's complex, we abort
            print("Could not proceed with Easy Apply form.")
            # Click dismiss
            dismiss_btn = page.locator("button.artdeco-modal__dismiss").all()
            if dismiss_btn:
                dismiss_btn[0].click()
                time.sleep(1)
                discard_btn = page.locator("button:has-text('Discard')").all()
                if discard_btn:
                    discard_btn[0].click()
            return False
            
    except Exception as e:
        print(f"Error during Easy Apply: {e}")
        return False
        
    return False
