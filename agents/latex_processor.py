import subprocess
import tempfile
import os
import shutil
from pathlib import Path

def extract_text_from_latex(uploaded_file):
    """Extract text from LaTeX file for processing"""
    content = uploaded_file.read().decode('utf-8')

    # Simple text extraction from LaTeX (remove common commands)
    import re

    # Remove comments
    content = re.sub(r'%.*', '', content)

    # Remove common LaTeX commands but keep content
    content = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})*', '', content)
    content = re.sub(r'[{}]', '', content)
    content = re.sub(r'\\\\', '\n', content)
    content = re.sub(r'\s+', ' ', content)

    # Clean up extra whitespace
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    return '\n'.join(lines)

def update_latex_resume(original_latex_content, optimized_text):
    """Update LaTeX resume with optimized content while preserving structure"""

    # This is a simplified approach - in production, you'd want more sophisticated LaTeX parsing
    # For now, we'll create a basic template with the optimized content

    latex_template = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}

\titleformat{\section}{\large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{1em}{}

\begin{document}

\pagestyle{empty}

""" + optimized_text.replace('\n\n', '\n\n\\vspace{0.2cm}\n\n') + r"""

\end{document}
"""

    return latex_template

def compile_latex_to_pdf(latex_content, output_filename="optimized_resume.pdf"):
    """Compile LaTeX content to PDF"""

    with tempfile.TemporaryDirectory() as temp_dir:
        # Write LaTeX content to temporary file
        tex_file = os.path.join(temp_dir, "resume.tex")
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        try:
            # Compile LaTeX to PDF
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
                capture_output=True,
                text=True,
                timeout=30
            )

            pdf_file = os.path.join(temp_dir, "resume.pdf")

            if os.path.exists(pdf_file):
                # Copy PDF to output location
                shutil.copy2(pdf_file, output_filename)
                return output_filename
            else:
                # If LaTeX compilation fails, return error info
                return f"LaTeX compilation failed: {result.stderr}"

        except subprocess.TimeoutExpired:
            return "LaTeX compilation timed out"
        except FileNotFoundError:
            return "pdflatex not found. Please install LaTeX distribution (e.g., TeX Live, MiKTeX)"
        except Exception as e:
            return f"Error during LaTeX compilation: {str(e)}"

def is_latex_available():
    """Check if LaTeX is available on the system"""
    try:
        result = subprocess.run(['pdflatex', '--version'], capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False
