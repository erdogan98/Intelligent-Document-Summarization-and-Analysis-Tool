import spacy
import logging
from typing import List, Tuple
import asyncio
from concurrent.futures import ProcessPoolExecutor
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the number of worker processes
MAX_WORKERS = os.cpu_count() or 4  # Fallback to 4 if os.cpu_count() is None

# Initialize a global ProcessPoolExecutor
executor = ProcessPoolExecutor(max_workers=MAX_WORKERS)


def load_spacy_model():
    """
    Loads the SpaCy transformer model. This function is intended to be called once per process.
    """
    try:
        nlp = spacy.load("en_core_web_trf")
        logger.info("SpaCy transformer model loaded successfully.")
        return nlp
    except Exception as e:
        logger.error(f"Error loading SpaCy model: {e}")
        raise


# Singleton pattern for model loading
# Each process will have its own instance of the model
def get_nlp():
    if not hasattr(get_nlp, "nlp"):
        get_nlp.nlp = load_spacy_model()
    return get_nlp.nlp


def extract_entities_sync(text: str) -> List[Tuple[str, str]]:
    """
    Synchronously extracts named entities from the input text using a transformer-based SpaCy model.

    Args:
        text (str): The input text to extract entities from.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing entity text and their labels.
    """
    try:
        nlp = get_nlp()
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        return []


async def extract_entities_async(text: str) -> List[Tuple[str, str]]:
    """
    Asynchronously extracts named entities from the input text using a transformer-based SpaCy model.

    Args:
        text (str): The input text to extract entities from.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing entity text and their labels.
    """
    loop = asyncio.get_running_loop()
    try:
        entities = await loop.run_in_executor(executor, extract_entities_sync, text)
        return entities
    except Exception as e:
        logger.error(f"Error in async entity extraction: {e}")
        return []
