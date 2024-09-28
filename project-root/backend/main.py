from fastapi import FastAPI, File, UploadFile
from starlette.responses import JSONResponse
from extract_text import extract_text
from load_t5 import summarize_text
from entity_recognition import extract_entities
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB_MODELS import Document
from fastapi.middleware.cors import CORSMiddleware
from sentiment import analyze_sentiment
import logging
import os
from TextInput import TextInput


logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.20:3000",
]

# Get allowed origins from environment variable
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# create database session
engine = create_engine('sqlite:///database.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Intelligent Document Summarization API"}


# handling file uploads
app.post("/upload")


async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename}


@app.post("/process")
async def process_document(file: UploadFile = File(...)):
    try:
        text = await extract_text(file)
    except Exception as e:
        logger.error(f"Error reading file {file.filename}: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Error reading the file."},
        )

    if text:
        summary = summarize_text(text)
        entities = extract_entities(text)
        sentiment = analyze_sentiment(text)
        logger.info(f"Processed file {file.filename} successfully.")
        return {
            "status": "success",
            "summary": summary,
            "entities": entities,
            "sentiment": sentiment,
        }
    else:
        logger.warning(f"No text extracted from file {file.filename}.")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Unsupported file type or error reading file"},
        )


@app.post("/process_text")
async def process_text(input: TextInput):
    """
    Endpoint to process raw text input.
    """
    text = input.text.strip()
    if not text:
        logger.warning("No text provided in the request.")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "No text provided."},
        )

    try:
        summary = summarize_text(text)
        entities = extract_entities(text)
        sentiment = analyze_sentiment(text)
        logger.info("Processed text input successfully.")
        return {
            "status": "success",
            "summary": summary,
            "entities": entities,
            "sentiment": sentiment,
        }
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Internal server error while processing text."},
        )
