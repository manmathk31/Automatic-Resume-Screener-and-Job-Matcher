import os

def process_resume(file_path: str):
    \"\"\"
    Mock for ML pipeline extracting text and structural data from PDF.
    Owner: Manmath
    \"\"\"
    # In reality, this would call PyMuPDF / pdfminer to extract text,
    # then NLP or LLM inference to parse skills and experience.
    return {
        "name": f"Candidate_{os.path.basename(file_path)}",
        "skills": ["Python", "Machine Learning", "NLP"],
        "experience_years": 4.5,
        "education": "BS Computer Science",
        "projects": ["Resume Screener"]
    }
