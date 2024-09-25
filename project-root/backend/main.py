from fastapi import FastAPI, File, UploadFile
from extract_text import extract_text
from load_t5 import summarize_text
from sentiment_analysis import analyze_sentiment
from entity_recognition import extract_entities
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB_MODELS import Document
app = FastAPI()

#create database session
engine = create_engine('sqlite:///database.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Intelligent Document Summarization API"}

#handling file uploads
app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename}

@app.post("/process")
async def process_document(file: UploadFile = File(...)):
    text = extract_text(file)
    if text:
        summary = summarize_text(text)
        entities = extract_entities(text)
        sentiment = analyze_sentiment(text)
        db = SessionLocal()
        doc = Document(
            filename=file.filename,
            content=text,
            summary=summary,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return {"status": "success", "data": doc.id}

