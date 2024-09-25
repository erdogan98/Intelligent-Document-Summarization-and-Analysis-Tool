# backend/routers/document.py

from fastapi import APIRouter, File, UploadFile
from utils.extract_text import extract_text
from utils.ml_functions import process_document

router = APIRouter()

@router.post("/process")
async def process_endpoint(file: UploadFile = File(...)):
    text = await extract_text(file)
    if text:
        result = await process_document(text, file.filename)
        return result
    else:
        return {"status": "error", "message": "Unsupported file type or extraction failed"}
