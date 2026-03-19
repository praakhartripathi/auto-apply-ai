def evaluate_job(job, resume_keywords):
    """
    Evaluates whether the job description contains enough matching keywords.
    """
    description = job.get("description", "").lower()
    
    if not description:
        return False
        
    match_count = 0
    for keyword in resume_keywords:
        if keyword.lower() in description:
            match_count += 1
            
    # Simple threshold: if at least 1 keyword matches, we'll try to apply
    # (The user requested: "as my resume matches appluy to all jobs")
    if match_count > 0:
        print(f"[Match] '{job.get('title')}' at {job.get('company')} matched {match_count} keywords.")
        return True
        
    print(f"[Skip] '{job.get('title')}' at {job.get('company')} did NOT match any keywords.")
    return False
