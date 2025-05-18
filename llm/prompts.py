def get_alignment_prompt(resume_text, job_desc):
    return f"""
You are an expert in enhancing resumes for Applicant Tracking Systems (ATS).
Rewrite the resume content below to better align with the job description.

- Include relevant keywords from the job description
- Keep the formatting and structure natural
- Make the candidate look like a perfect fit
- Return only updated content (no comments or explanations)

Resume:
{resume_text}

Job Description:
{job_desc}
"""
