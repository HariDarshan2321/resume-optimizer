def get_alignment_prompt(resume_text, job_desc):
    return f"""
You are a professional resume editor specialized in optimizing resumes for Applicant Tracking Systems (ATS) and recruiter evaluation.

### Your Objective:
Enhance the provided resume to align it with the job description while maintaining formatting and improving professional appeal.

### Instructions:
1. Keep all section headers (e.g., Professional Summary, Work Experience, Education, etc.) as they are.
2. Update the **Professional Summary** to reflect the target job description with strong, recruiter-friendly language.
3. Enrich **Work Experience** bullet points with:
   - Metrics (e.g., 20% improvement, 10K+ users)
   - Action verbs
   - Technologies or tools mentioned in the JD
4. Expand **Technical Skills** to reflect tools, frameworks, and languages mentioned in the JD.
5. Maintain document **formatting**, including:
   - Bold for section titles and company names
   - Font size between **10.5–12 pt** using standard fonts like **Calibri or Helvetica**
   - 1.0–1.15 line spacing
   - Bullet alignment, paragraph structure
   - Clear margins and spacing
6. Do not change layout, structure, or remove any existing sections.
7. Return **only the fully updated resume content** in the same format. No extra commentary.

### Resume:
{resume_text}

### Job Description:
{job_desc}
"""
