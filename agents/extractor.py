import fitz
from docx import Document
import tempfile

def extract_text_from_file(uploaded_file):
    suffix = uploaded_file.name.split('.')[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix='.' + suffix) as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    if suffix == 'pdf':
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])
    elif suffix == 'docx':
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return "Unsupported format"
