import pdfplumber
import spacy
from .APIKeyFile import Api_key
from groq import Groq
import json


def extract_text_from_pdf(pdf_path):
    text=""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text+=page.extract_text()+"\n"
    return text.strip()


def analyze_resume_with_llm(resume_text: str, job_description: str) -> dict:
    prompt = f"""
        You are an ATS (Applicant Tracking System). Evaluate the following resume against the job description.

        ### Job Description:
        {job_description}

        ### Resume:
        {resume_text}

        ### Rules:
        1. Extract skills **only from the 'Skills Summary' section** of the resume. 
        - Ignore technologies mentioned in project descriptions unless they also appear in the Skills Summary.
        2. Extract years of professional experience (approximate if not exact and show 0 if there is no experience section in resume).
        3. Extract only project names from the 'Projects' section.
        4. Return output strictly as valid JSON with these keys:
        - rank (integer 0-100)
        - skills (list of strings)
        - experience (float in years)
        - projects (list of project names)

        ### Example Output:
        {{
        "rank": 85,
        "skills": ["Python", "C++", "SQL", "Java", "Dart", "Flutter", "Django"],
        "experience": 1,
        "projects": ["Crime Reporting App", "Task Management App", "Hotel Booking System"]
        }}
        """


    try:
        client = Groq(api_key=Api_key)
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        return json.loads(result)
    except Exception as e:
        print(e)
        return {"rank": 0, "skills": [], "experience": 0, "projects": []}

def process_resume(pdf_path,job_description):
    try:    
        pdf_text=extract_text_from_pdf(pdf_path)
        result=analyze_resume_with_llm(pdf_text,job_description)
        return result
    except Exception as e:
        print(e)
        return None