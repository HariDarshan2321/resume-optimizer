from llm.prompts import get_alignment_prompt
from utils.model_utils import call_groq

def align_resume_with_job(resume_text, job_desc):
    prompt = get_alignment_prompt(resume_text, job_desc)
    return call_groq(prompt)
