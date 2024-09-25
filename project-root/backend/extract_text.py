from fastapi import UploadFile
import PyPDF2
import docx2txt

def extract_text(file: UploadFile):
    if file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.filename.endswith('.docx'):
        text = docx2txt.process(file.file)
        return text
    else:
        return None