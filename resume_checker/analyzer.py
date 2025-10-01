import pdfplumber
import spacy
from .APIKeyFile import Api_key

def extract_text_from_pdf(pdf_path):
    text=""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text+=page.extract_text()+"\n"
    return text.strip()

def analyze_resume_with_llm(resume_text:str,job_decription:str)->dict:
    prompt = f"""
        You are an AI-powered Applicant Tracking System (ATS). 
        Your job is to carefully evaluate resumes against a given job description.

        ### Job Description:
        {job_description}

        ### Resume:
        {resume_text}

        ### Instructions:
        1. Compare the resume with the job description.
        2. Score the resume from 0 to 100, based on overall relevance.
        3. Extract key information from the resume:
        - Relevant skills that match the job description
        - Years of professional experience (approximate if not exact)
        - Relevant academic or personal projects
        4. Focus only on **job-related information** (ignore unrelated details).
        5. Output must be **valid JSON only**, with no explanations.

        ### Expected JSON format:
        {{
        "rank": <integer between 0-100>,
        "skills": ["skill1", "skill2", "skill3"],
        "experience": <integer in years>,
        "projects": ["project1", "project2"]
        }}
        """
