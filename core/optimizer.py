import PyPDF2
import re

def extract_keywords_from_pdf(pdf_path):
    print(f"Extracting skills from {pdf_path}...")
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for i in range(len(reader.pages)):
                text += reader.pages[i].extract_text()
                
        # A simple predefined list of tech keywords to look for
        common_tech = [
            "python", "java", "c++", "c#", "javascript", "typescript", "react", "angular", 
            "vue", "node", "express", "aws", "azure", "gcp", "docker", "kubernetes", "sql", 
            "mysql", "postgresql", "nosql", "mongodb", "spring", "spring boot", "django", 
            "flask", "machine learning", "ai", "api", "rest", "graphql", "automation", 
            "selenium", "playwright", "ci/cd", "jenkins", "git", "linux"
        ]
                       
        text_lower = text.lower()
        found_keywords = [kw for kw in common_tech if kw in text_lower]
        print(f"Detected skills in resume: {found_keywords}")
        
        # If the resume is completely empty of these keywords, return a default generic list
        return found_keywords if found_keywords else ["software", "developer", "engineer"]
        
    except FileNotFoundError:
        print(f"Resume file '{pdf_path}' not found! Make sure the file exists in the root directory.")
        return ["software", "developer", "engineer"]
    except Exception as e:
        print(f"Could not parse PDF '{pdf_path}': {e}")
        return ["software", "developer", "engineer"]
