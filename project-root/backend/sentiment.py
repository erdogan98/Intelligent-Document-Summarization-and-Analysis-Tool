from transformers import pipeline
import logging
import nltk
import re
import emoji
import torch

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download necessary NLTK data
nltk.download('punkt', quiet=True)

# Initialize the sentiment analysis pipeline with a transformer-based model
# You can choose different models based on your requirements
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    tokenizer="distilbert-base-uncased-finetuned-sst-2-english",
    framework="pt",  # Use "tf" for TensorFlow backend
    device=0 if torch.cuda.is_available() else -1  # Use GPU if available
)


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

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove mentions and hashtags
    text = re.sub(r'[@#]\w+', '', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    max_chars=2000
    if len(text) > max_chars:
        text = text[:max_chars]

    return text


def analyze_sentiment(text: str):
    """
    Analyzes the sentiment of the input text using a transformer-based model.

    Args:
        text (str): The input text to analyze.

    Returns:
        dict: Sentiment analysis results.
    """
    try:
        # Preprocess the text
        cleaned_text = preprocess_text(text)

        # Ensure the text is not empty after preprocessing
        if not cleaned_text:
            logger.warning("Input text is empty after preprocessing.")
            return {"label": "NEUTRAL", "score": 0.0,"compound":0.0}

        # Perform sentiment analysis
        results = sentiment_pipeline(cleaned_text)

        # If the input is too long, the pipeline might split it into chunks
        # We'll aggregate the results
        if isinstance(results, list):
            # Simple aggregation: majority vote
            labels = [res['label'] for res in results]
            scores = [res['score'] for res in results]

            # Calculate weighted average
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
                            len(positive_scores) + len(negative_scores))

            return {"label": final_label, "score": final_score}
        else:
            # Single result
            return results
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")
        return {"label": "ERROR", "score": 0.0}