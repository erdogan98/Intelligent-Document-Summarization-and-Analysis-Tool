import asyncio

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from starlette.responses import JSONResponse
from extract_text import extract_text
from load_t5 import summarize_text
from entity_recognition import extract_entities  # Ensure correct module name
from sentiment import analyze_sentiment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from DB_MODELS import Document  # Ensure DB_MODELS.py defines Document model
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

# Get allowed origins from environment variable or use default
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.0.20:3000",
    ]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Specifies the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database engine and session
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Pydantic model for text input
class TextInput(BaseModel):
    text: str


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Intelligent Document Summarization API"}


# Correctly define the /upload endpoint
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        content = await file.read()
        return {"filename": file.filename, "content_length": len(content)}
    except Exception as e:
        logger.error(f"Error uploading file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during file upload.")


@app.post("/process")
async def process_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Extract text from the uploaded file
        text = await extract_text(file)
    except HTTPException as he:
        logger.error(f"HTTPException while extracting text from {file.filename}: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error reading file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error reading the file.")

    if text:
        try:
            # Initiate asynchronous tasks
            summary_task = (summarize_text(text))
            entities_task = (extract_entities(text))
            sentiment_task = (analyze_sentiment(text))

            # Await all tasks concurrently
            summary, entities, sentiment = summary_task, entities_task, sentiment_task

            # # Optionally, save to database
            # document = Document(filename=file.filename, text=text, summary=summary, entities=entities, sentiment=sentiment)
            # db.add(document)
            # db.commit()
            # db.refresh(document)

            logger.info(f"Processed file {file.filename} successfully.")
            return {
                "status": "success",
                "summary": summary,
                "entities": entities,
                "sentiment": sentiment,
            }
        except Exception as e:
            logger.error(f"Error processing document {file.filename}: {e}")
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Internal server error while processing document."},
            )
    else:
        logger.warning(f"No text extracted from file {file.filename}.")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Unsupported file type or error reading file."},
        )


@app.post("/process_text")
async def process_text(input: TextInput, db: Session = Depends(get_db)):
    """
    Endpoint to process raw text input.
    """
    text = input.text.strip()
    if not text:
        logger.warning("No text provided in the request.")
        raise HTTPException(status_code=400, detail="No text provided.")

    try:
        # Initiate asynchronous tasks
        summary_task = (summarize_text(text))
        entities_task = (extract_entities(text))
        sentiment_task = (analyze_sentiment(text))

        # Await all tasks concurrently
        summary, entities, sentiment = summary_task, entities_task, sentiment_task

        # # Optionally, save to database
        # document = Document(filename="Raw Text Input", text=text, summary=summary, entities=entities, sentiment=sentiment)
        # db.add(document)
        # db.commit()
        # db.refresh(document)

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
