from docx import Document

def build_docx(content: str, filename="optimized_resume.docx"):
    doc = Document()
    for line in content.split('\n'):
        doc.add_paragraph(line)
    doc.save(filename)
    return filename
