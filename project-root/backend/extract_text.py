import aiofiles
import PyPDF2
import docx2txt
from striprtf.striprtf import rtf_to_text
from bs4 import BeautifulSoup
import logging
from fastapi import UploadFile
from starlette.concurrency import run_in_threadpool

logger = logging.getLogger(__name__)


async def extract_text(file: UploadFile) -> str:
    try:
        filename = file.filename.lower()

        if filename.endswith('.pdf'):
            return await extract_pdf(file)
        elif filename.endswith('.docx'):
            return await extract_docx(file)
        elif filename.endswith('.txt'):
            return await extract_txt(file)
        elif filename.endswith('.rtf'):
            return await extract_rtf(file)
        elif filename.endswith('.md'):
            return await extract_markdown(file)
        elif filename.endswith(('.html', '.htm')):
            return await extract_html(file)
        else:
            logger.warning(f"Unsupported file type: {file.filename}")
            return None
    except Exception as e:
        logger.error(f"Error extracting text from {file.filename}: {e}")
        return None


async def extract_pdf(file: UploadFile) -> str:
    def _extract():
        reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
        return text

    text = await run_in_threadpool(_extract)
    return text


async def extract_docx(file: UploadFile) -> str:
    def _extract():
        text = docx2txt.process(file.file)
        return text

    text = await run_in_threadpool(_extract)
    return text


async def extract_txt(file: UploadFile) -> str:
    async with aiofiles.open(f"/tmp/{file.filename}", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    async with aiofiles.open(f"/tmp/{file.filename}", 'r', encoding='utf-8') as in_file:
        text = await in_file.read()
    return text


async def extract_rtf(file: UploadFile) -> str:
    def _extract():
        content = file.file.read().decode('utf-8', errors='ignore')
        text = rtf_to_text(content)
        return text

    text = await run_in_threadpool(_extract)
    return text


async def extract_markdown(file: UploadFile) -> str:
    async with aiofiles.open(f"/tmp/{file.filename}", 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    async with aiofiles.open(f"/tmp/{file.filename}", 'r', encoding='utf-8') as in_file:
        text = await in_file.read()

    # Optionally, you can strip Markdown syntax if desired
    # For simplicity, we'll return the raw Markdown text
    return text


async def extract_html(file: UploadFile) -> str:
    async with aiofiles.open(f"/tmp/{file.filename}", 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    async with aiofiles.open(f"/tmp/{file.filename}", 'r', encoding='utf-8') as in_file:
        html_content = await in_file.read()

    def _extract():
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator='\n')
        return text

    text = await run_in_threadpool(_extract)
    return text
