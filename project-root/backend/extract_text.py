from fastapi import UploadFile
import PyPDF2
import docx2txt

async def extract_text(file: UploadFile):
    try:
        if file.filename.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file.file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        elif file.filename.endswith('.docx'):
            text = docx2txt.process(file.file)
            return text
        elif file.filename.endswith('.txt'):
            content = await file.read()
            return content.decode('utf-8')
        else:
            return None
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
