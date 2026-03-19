import time

def process_jobs(page, keyword, location, resume_keywords, apply_function, limit, tracker=None):
    print(f"Searching for '{keyword}' in '{location}'...")
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
    page.goto(url)
    
    try:
        page.wait_for_selector(".jobs-search-results-list", timeout=15000)
    except:
        print("No job results found or page took too long to load.")
        return 0

    applied_count = 0
    job_cards = page.locator(".job-card-container").all()
    print(f"Found {len(job_cards)} jobs on this page.")
    
    for idx, card in enumerate(job_cards):
        if applied_count >= limit:
            break
            
        try:
            card.scroll_into_view_if_needed()
            card.click()
            time.sleep(2) # Wait for job details pane to load
            
            # Extract basic info
            title_el = page.locator(".job-details-jobs-unified-top-card__job-title").first
            company_el = page.locator(".job-details-jobs-unified-top-card__company-name").first
            description_el = page.locator("#job-details").first
            
            title = title_el.inner_text() if title_el.count() > 0 else "Unknown Title"
            company = company_el.inner_text() if company_el.count() > 0 else "Unknown Company"
            description = description_el.inner_text() if description_el.count() > 0 else ""
            
            easy_apply_btn = page.locator("button:has-text('Easy Apply')").count() > 0
            
            print(f"\n--- Job {idx+1}: {title} at {company} ---")
            
            # Match
            match_count = sum(1 for kw in resume_keywords if kw.lower() in description.lower())
            
            if match_count > 0:
                print(f"[Match] Matched {match_count} keywords from your resume.")
                if easy_apply_btn:
                    print("Attempting Easy Apply...")
                    success = apply_function(page)
                    if success:
                        applied_count += 1
                        if tracker:
                            tracker.log_application(title, company)
                else:
                    print("No Easy Apply button available. Skipping.")
            else:
                print(f"[Skip] Did NOT match your resume keywords.")
                
        except Exception as e:
            print(f"Error processing job card: {e}")
            continue

    return applied_count
