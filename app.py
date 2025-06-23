import streamlit as st
from agents.extractor import extract_text_from_file
from agents.aligner import align_resume_with_job
from agents.formatter import build_docx
from agents.latex_processor import extract_text_from_latex, update_latex_resume, compile_latex_to_pdf, is_latex_available
from agents.job_scraper import get_job_description_from_url
from utils.feedback_system import show_feedback_popup, trigger_feedback_popup
import os

# Page configuration
st.set_page_config(
    page_title="AI Resume Optimizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header"> AI Resume Optimizer for ATS</h1>', unsafe_allow_html=True)

# Sidebar for options
with st.sidebar:
    st.header("Options")

    # Resume format selection
    resume_format = st.radio(
        "Choose your resume format:",
        ["Standard (PDF/DOCX)", "Custom LaTeX Template"],
        help="Select 'Custom LaTeX Template' if you want to upload your own LaTeX resume format"
    )

    # Job description input method
    job_input_method = st.radio(
        "How would you like to provide the job description?",
        ["Paste Text", "URL Scraping"],
        help="Choose 'URL Scraping' to automatically extract job description from job posting URLs"
    )

    # LaTeX availability check
    if resume_format == "Custom LaTeX Template":
        if is_latex_available():
            st.success("✅ LaTeX is available")
        else:
            st.error("❌ LaTeX not found. Please install a LaTeX distribution (e.g., TeX Live, MiKTeX)")
            st.info("LaTeX is required for custom template processing")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Upload Your Resume")

    if resume_format == "Standard (PDF/DOCX)":
        resume_file = st.file_uploader(
            "Upload your resume (.pdf or .docx)",
            type=["pdf", "docx"],
            help="Upload your current resume in PDF or DOCX format"
        )
    else:
        resume_file = st.file_uploader(
            "Upload your LaTeX resume (.tex)",
            type=["tex"],
            help="Upload your LaTeX resume template"
        )

        if resume_file and not is_latex_available():
            st.error("LaTeX is not available on this system. Please install LaTeX or use the standard format.")
            resume_file = None

with col2:
    st.subheader("Job Description")

    job_description = ""

    if job_input_method == "Paste Text":
        job_description = st.text_area(
            "Paste the Job Description",
            height=200,
            placeholder="Copy and paste the job description here...",
            help="Paste the complete job description including requirements, responsibilities, and qualifications"
        )
    else:
        job_url = st.text_input(
            "Enter Job Posting URL",
            placeholder="https://linkedin.com/jobs/view/...",
            help="Enter the URL of the job posting (LinkedIn, Indeed, Glassdoor, etc.)"
        )

        if job_url:
            if st.button("🔍 Extract Job Description", type="secondary"):
                with st.spinner("Extracting job description from URL..."):
                    job_description = get_job_description_from_url(job_url)

                    if job_description.startswith("Error"):
                        st.error(job_description)
                        job_description = ""
                    else:
                        st.success("✅ Job description extracted successfully!")

                        # Show extracted content in an expander
                        with st.expander("📋 Extracted Job Description", expanded=False):
                            st.text_area("", value=job_description, height=200, disabled=True)

# Processing section
st.markdown("---")
st.subheader("🔄 Process Resume")

# Show current inputs status
col_status1, col_status2, col_status3 = st.columns(3)

with col_status1:
    if resume_file:
        st.success("✅ Resume uploaded")
    else:
        st.warning("⏳ Upload resume")

with col_status2:
    if job_description:
        st.success("✅ Job description ready")
    else:
        st.warning("⏳ Provide job description")

with col_status3:
    if resume_format == "Custom LaTeX Template" and not is_latex_available():
        st.error("❌ LaTeX not available")
    else:
        st.success("✅ System ready")

# Main processing button
if st.button("Optimize Resume", type="primary", disabled=not (resume_file and job_description)):
    if resume_file and job_description:
        with st.spinner("Analyzing and optimizing your resume..."):
            try:
                # Extract text based on format
                if resume_format == "Standard (PDF/DOCX)":
                    ext_text = extract_text_from_file(resume_file)
                else:
                    ext_text = extract_text_from_latex(resume_file)

                # Align resume with job description
                optimized_text = align_resume_with_job(ext_text, job_description)

                # Generate output based on format
                if resume_format == "Standard (PDF/DOCX)":
                    output_path = build_docx(optimized_text)
                    file_extension = "docx"
                    mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                else:
                    # For LaTeX format
                    original_content = resume_file.read().decode('utf-8')
                    latex_content = update_latex_resume(original_content, optimized_text)
                    output_path = compile_latex_to_pdf(latex_content)

                    if output_path.endswith('.pdf'):
                        file_extension = "pdf"
                        mime_type = "application/pdf"
                    else:
                        # Error occurred
                        st.error(f"LaTeX compilation failed: {output_path}")
                        st.stop()

                # Success message
                st.markdown('<div class="success-box">✅ <strong>Resume optimization completed successfully!</strong></div>', unsafe_allow_html=True)

                # Download section
                col_download, col_preview = st.columns([1, 1])

                with col_download:
                    with open(output_path, "rb") as f:
                        download_button = st.download_button(
                            label=f"Download Optimized Resume (.{file_extension})",
                            data=f,
                            file_name=f"optimized_resume.{file_extension}",
                            mime=mime_type,
                            type="primary"
                        )

                        # Trigger feedback popup when download button is clicked
                        if download_button:
                            trigger_feedback_popup()

                with col_preview:
                    # Show optimization summary
                    with st.expander("Optimization Summary", expanded=True):
                        st.write("**Changes made:**")
                        st.write("• Enhanced professional summary")
                        st.write("• Optimized keywords for ATS")
                        st.write("• Improved formatting and structure")
                        st.write("• Aligned content with job requirements")

                # Show optimized content preview
                with st.expander("📄 Preview Optimized Content", expanded=False):
                    st.text_area("Optimized Resume Content", value=optimized_text, height=300, disabled=True)

            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")
                st.info("Please try again or contact support if the issue persists.")

# Feedback section
show_feedback_popup()

# Footer with additional information
st.markdown("---")
st.markdown("""
### Features:
- **ATS Optimization**: Ensures your resume passes Applicant Tracking Systems
- **Custom LaTeX Support**: Upload your own LaTeX templates for personalized formatting
- **URL Job Scraping**: Automatically extract job descriptions from popular job sites
- **AI-Powered Alignment**: Smart content optimization based on job requirements
- **Multiple Formats**: Support for PDF, DOCX, and LaTeX formats

### Tips for Best Results:
1. **Use complete job descriptions** for better optimization
2. **Review the optimized content** before submitting
3. **Customize further** based on your specific experience
4. **Test with different job descriptions** to see variations

### Supported Job Sites:
LinkedIn • Indeed • Glassdoor • Monster • CareerBuilder • ZipRecruiter • AngelList • Stack Overflow Jobs
""")

# Technical information in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🛠️ Technical Info")
    st.info(f"**LaTeX Status**: {'✅ Available' if is_latex_available() else '❌ Not Available'}")
    st.info("**AI Model**: Llama 3.3 70B")
    st.info("**Supported Formats**: PDF, DOCX, LaTeX")
