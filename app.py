import streamlit as st
from agents.extractor import extract_text_from_file
from agents.aligner import align_resume_with_job
from agents.formatter import build_docx
import os

st.title("Agentic AI Resume Optimizer for ATS")

resume_file = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])
job_description = st.text_area("Paste the Job Description")

if st.button("Optimize Resume") and resume_file and job_description:
    with st.spinner("Analyzing and optimizing your resume..."):
        ext_text = extract_text_from_file(resume_file)
        optimized_text = align_resume_with_job(ext_text, job_description)
        output_path = build_docx(optimized_text)

        with open(output_path, "rb") as f:
            st.download_button("Download Optimized Resume", f, file_name="optimized_resume.docx")
