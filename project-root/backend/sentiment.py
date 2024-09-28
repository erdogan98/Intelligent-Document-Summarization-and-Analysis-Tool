# sentiment.py

import logging
import torch
import nltk
import re
import emoji
from transformers import pipeline
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
import asyncio
import os
import atexit
from functools import lru_cache

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download necessary NLTK data
nltk.download('punkt', quiet=True)

# Environment Variables for Configuration
BATCH_SIZE = int(os.getenv("SENTIMENT_BATCH_SIZE", 8))  # Default to 8 if not set
MAX_WORKERS = int(os.getenv("SENTIMENT_MAX_WORKERS", 4))  # Number of threads for sentiment analysis

# Initialize a global ThreadPoolExecutor for asynchronous operations
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

# Register shutdown handler to gracefully close the executor
atexit.register(lambda: executor.shutdown(wait=True))

# Singleton pattern for sentiment_pipeline
def get_sentiment_pipeline():
    if not hasattr(get_sentiment_pipeline, "pipeline"):
        try:
            device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
            get_sentiment_pipeline.pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                tokenizer="distilbert-base-uncased-finetuned-sst-2-english",
                framework="pt",  # Use PyTorch backend for better performance
                device=device,
                batch_size=BATCH_SIZE  # Configurable via environment variable
            )
            logger.info(f"Sentiment pipeline initialized on device {device}.")
        except Exception as e:
            logger.error(f"Error initializing sentiment pipeline: {e}")
            raise
    return get_sentiment_pipeline.pipeline

def preprocess_text(text: str) -> str:
    """
    Preprocesses the input text by cleaning and handling special characters.

    Args:
        text (str): The raw input text.

    Returns:
        str: The preprocessed text.
    """
    # Convert emojis to text
    text = emoji.demojize(text, delimiters=(" ", " "))

    # Remove URLs, mentions, and hashtags in a single regex operation
    text = re.sub(r'(http\S+)|([@#]\w+)', '', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Truncate the text to a maximum of 2000 characters
    max_chars = 2000
    if len(text) > max_chars:
        text = text[:max_chars]

    return text

@lru_cache(maxsize=1024)
def cached_analyze_sentiment_sync(text: str) -> Dict[str, float]:
    """
    Caches the sentiment analysis results for previously processed texts.

    Args:
        text (str): The input text to analyze.

    Returns:
        Dict[str, float]: Sentiment analysis results.
    """
    return analyze_sentiment_sync(text)

def analyze_sentiment_sync(text: str) -> Dict[str, float]:
    """
    Synchronously analyzes the sentiment of the input text using a transformer-based model.

    Args:
        text (str): The input text to analyze.

    Returns:
        Dict[str, float]: Sentiment analysis results.
    """
    try:
        # Preprocess the text
        cleaned_text = preprocess_text(text)

        # Ensure the text is not empty after preprocessing
        if not cleaned_text:
            logger.warning("Input text is empty after preprocessing.")
            return {"label": "NEUTRAL", "score": 0.0}

        # Perform sentiment analysis
        results = get_sentiment_pipeline()(cleaned_text)

        # If the input is too long, the pipeline might split it into chunks
        # Aggregate the results
        if isinstance(results, list):
            # Extract labels and scores
            labels = [res['label'] for res in results]
            scores = [res['score'] for res in results]

            # Calculate weighted average for positive and negative sentiments
            positive_scores = [score for label, score in zip(labels, scores) if label == "POSITIVE"]
            negative_scores = [score for label, score in zip(labels, scores) if label == "NEGATIVE"]

            if positive_scores and not negative_scores:
                final_label = "POSITIVE"
                final_score = sum(positive_scores) / len(positive_scores)
            elif negative_scores and not positive_scores:
                final_label = "NEGATIVE"
                final_score = sum(negative_scores) / len(negative_scores)
            else:
                # Mixed sentiments
                final_label = "MIXED"
                final_score = (sum(positive_scores) - sum(negative_scores)) / (
                    len(positive_scores) + len(negative_scores)
                )

            return {"label": final_label, "score": final_score}
        else:
            # Single result
            return results
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")
        return {"label": "ERROR", "score": 0.0}

async def analyze_sentiment_async(text: str) -> Dict[str, float]:
    """
    Asynchronously analyzes the sentiment of the input text using a transformer-based model.

    Args:
        text (str): The input text to analyze.

    Returns:
        Dict[str, float]: Sentiment analysis results.
    """
    loop = asyncio.get_running_loop()
    try:
        sentiment = await loop.run_in_executor(executor, cached_analyze_sentiment_sync, text)
        return sentiment
    except Exception as e:
        logger.error(f"Error in asynchronous sentiment analysis: {e}")
        return {"label": "ERROR", "score": 0.0}
