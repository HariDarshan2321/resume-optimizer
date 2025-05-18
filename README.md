# AI Resume Optimizer for ATS (Streamlit + LLM + PDF/DOCX)

This project helps job seekers improve their resumes by automatically aligning them to a specific job description using an AI-powered agent workflow. It ensures the resume is optimized for Applicant Tracking Systems (ATS) and human recruiters while preserving formatting, layout, and professional styling.


## 🚀 Features

- Upload `.pdf` resumes
- Paste a job description
- Automatically extract resume content
- Enhance the resume with relevant skills, technologies, and keywords
- Output a downloadable `.docx` resume with updated content
- Built-in multi-agent architecture for extraction, alignment, and formatting
- Deployed via Streamlit

---

## 🛠️ Tech Stack

| Component         | Tool/Library              |
|------------------|---------------------------|
| Frontend UI       | Streamlit                 |
| Resume Parsing    | PyMuPDF, python-docx      |
| LLM Integration   | Groq                      |
| Multi-Agent Flow  | LangChain and custom logic|
| Formatting        | `python-docx`             |

---


## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/HariDarshan2321/resume-optimizer.git
cd resume-optimizer

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```bash
Create a .env file in the root directory:
and add ypur
GROQ_API_KEY=your_groq_api_key_here

