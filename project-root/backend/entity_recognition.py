import spacy
import logging
from typing import List, Tuple

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the transformer-based SpaCy model
try:
    nlp = spacy.load("en_core_web_trf")
    logger.info("SpaCy transformer model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading SpaCy model: {e}")
    raise

def extract_entities(text: str) -> List[Tuple[str, str]]:
    """
    Extracts named entities from the input text using a transformer-based SpaCy model.

    Args:
        text (str): The input text to extract entities from.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing entity text and their labels.
    """
    try:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        return []
