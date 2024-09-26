import os
import openai
import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from gensim.summarization import keywords
from langdetect import detect
from transformers import pipeline

# Load models and data
nlp_spacy = spacy.load("en_core_web_sm")
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
summarizer = pipeline("summarization", model="t5-base")

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

async def summarize_text(text):
    # Using OpenAI's GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following text:\n\n{text}",
        max_tokens=500,
        temperature=0.5,
    )
    summary = response.choices[0].text.strip()
    return summary

def extract_entities(text):
    doc = nlp_spacy(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def analyze_sentiment(text):
    sentiment = sia.polarity_scores(text)
    return sentiment

def extract_keywords(text):
    key_words = keywords(text).split('\n')
    return key_words

def detect_language(text):
    language = detect(text)
    return language

async def process_document(text, filename):
    try:
        summary = await summarize_text(text)
        entities = extract_entities(text)
        sentiment = analyze_sentiment(text)
        keywords_list = extract_keywords(text)
        language = detect_language(text)

        result = {
            "status": "success",
            "filename": filename,
            "content": text,
            "summary": summary,
            "entities": entities,
            "sentiment": sentiment,
            "keywords": keywords_list,
            "language": language,
        }
        return result
    except Exception as e:
        print(f"Error processing document: {e}")
        return {"status": "error", "message": "Processing failed"}
