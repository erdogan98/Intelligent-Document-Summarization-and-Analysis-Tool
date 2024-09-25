from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str):
    sentiment = sia.polarity_scores(text)
    return sentiment
