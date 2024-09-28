
import aiofiles
import PyPDF2
from docx import Document
from striprtf.striprtf import rtf_to_text
from bs4 import BeautifulSoup
import logging
from fastapi import UploadFile, HTTPException
from starlette.concurrency import run_in_threadpool
from pathlib import Path
import tempfile
import markdown

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define maximum file size (e.g., 10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Define a safe temporary directory
SAFE_TMP_DIR = Path(tempfile.gettempdir()) / "extracted_files"
SAFE_TMP_DIR.mkdir(parents=True, exist_ok=True)


def get_safe_filename(filename: str) -> str:
    """
    Sanitizes the filename to prevent path traversal attacks.

    Args:
        filename (str): Original filename.

    Returns:
        str: Sanitized filename.
    """
    return Path(filename).name


async def extract_text(file: UploadFile) -> str:
    """
    Determines the file type and extracts text accordingly.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        str: Extracted text.

    Raises:
        HTTPException: If the file type is unsupported or an error occurs during extraction.
    """
    # Sanitize the filename
    safe_filename = get_safe_filename(file.filename).lower()

    # Read all content to check the file size
    content = await file.read()
    file_size = len(content)
    if file_size > MAX_FILE_SIZE:
        logger.warning(f"File too large: {file.filename}")
        raise HTTPException(status_code=400, detail="File too large")

    # Reset the file pointer to the beginning for further processing
    await file.seek(0)

    # Map file extensions to their respective extractor functions
    extractors = {
        '.pdf': extract_pdf,
        '.docx': extract_docx,
        '.txt': extract_txt,
        '.rtf': extract_rtf,
        '.md': extract_markdown,
        '.html': extract_html,
        '.htm': extract_html,
    }

    for ext, extractor in extractors.items():
        if safe_filename.endswith(ext):
            logger.info(f"Extracting text from {file.filename} as {ext} file.")
            return await extractor(file)

    logger.warning(f"Unsupported file type: {file.filename}")
    raise HTTPException(status_code=400, detail="Unsupported file type")


async def extract_pdf(file: UploadFile) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file (UploadFile): The uploaded PDF file.

    Returns:
        str: Extracted text.
    """
    try:
        def _extract():
            reader = PyPDF2.PdfReader(file.file)
            if reader.is_encrypted:
                try:
                    reader.decrypt('')
                    logger.info(f"Decrypted PDF: {file.filename}")
                except Exception as e:
                    logger.error(f"Failed to decrypt PDF {file.filename}: {e}")
                    return ""
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text

        text = await run_in_threadpool(_extract)
        return text
    except PyPDF2.errors.PdfReadError as e:
        logger.error(f"PDF read error for {file.filename}: {e}")
        raise HTTPException(status_code=400, detail="Invalid PDF file")
    except Exception as e:
        logger.error(f"Unexpected error in PDF extraction for {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error extracting PDF content")


async def extract_docx(file: UploadFile) -> str:
    """
    Extracts text from a DOCX file.

    Args:
        file (UploadFile): The uploaded DOCX file.

    Returns:
        str: Extracted text.
    """
    try:
        def _extract():
            document = Document(file.file)
            return "\n".join(para.text for para in document.paragraphs)

        text = await run_in_threadpool(_extract)
        return text
    except Exception as e:
        logger.error(f"Error extracting DOCX from {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error extracting DOCX content")


async def extract_txt(file: UploadFile) -> str:
    """
    Extracts text from a TXT file.

    Args:
        file (UploadFile): The uploaded TXT file.

    Returns:
        str: Extracted text.
    """
    try:
        content = await file.read()
        text = content.decode('utf-8', errors='ignore')
        return text
    except Exception as e:
        logger.error(f"Error extracting TXT from {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error extracting TXT content")


async def extract_rtf(file: UploadFile) -> str:
    """
    Extracts text from an RTF file.

    Args:
        file (UploadFile): The uploaded RTF file.

    Returns:
        str: Extracted text.
    """
    try:
        def _extract():
            content_bytes = file.file.read()
            content = content_bytes.decode('utf-8', errors='ignore')
            return rtf_to_text(content)

        text = await run_in_threadpool(_extract)
        return text
    except Exception as e:
        logger.error(f"Error extracting RTF from {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error extracting RTF content")


async def extract_markdown(file: UploadFile) -> str:
    """
    Extracts text from a Markdown file by converting it to HTML first.

    Args:
        file (UploadFile): The uploaded Markdown file.

    Returns:
        str: Extracted text.
    """
    try:
        content = await file.read()
        markdown_content = content.decode('utf-8', errors='ignore')

        def _extract():
            html = markdown.markdown(markdown_content)
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text(separator='\n')

        text = await run_in_threadpool(_extract)
        return text
    except Exception as e:
        logger.error(f"Error extracting Markdown from {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error extracting Markdown content")


async def extract_html(file: UploadFile) -> str:
    """
    Extracts text from an HTML file.

    Args:
        file (UploadFile): The uploaded HTML file.

    Returns:
        str: Extracted text.
    """
    try:
        content = await file.read()
        html_content = content.decode('utf-8', errors='ignore')

        def _extract():
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator='\n')

        text = await run_in_threadpool(_extract)
        return text
    except Exception as e:
        logger.error(f"Error extracting HTML from {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error extracting HTML content")
