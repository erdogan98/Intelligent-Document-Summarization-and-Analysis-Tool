# load_t5.py

import logging
import torch
import nltk
from typing import List
from transformers import pipeline, T5Tokenizer
from concurrent.futures import ThreadPoolExecutor
import asyncio
import os
import atexit

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download NLTK data for sentence tokenization if not already present
nltk.download('punkt', quiet=True)

# Environment Variables for Configuration
BATCH_SIZE = int(os.getenv("SUMMARIZER_BATCH_SIZE", 8))  # Default to 8 if not set
MAX_WORKERS = int(os.getenv("SUMMARIZER_MAX_WORKERS", 4))  # Number of threads for summarization

# Initialize a global ThreadPoolExecutor for asynchronous operations
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

# Register shutdown handler to gracefully close the executor
atexit.register(lambda: executor.shutdown(wait=True))

# Singleton pattern for tokenizer and summarizer
def get_tokenizer():
    if not hasattr(get_tokenizer, "tokenizer"):
        try:
            get_tokenizer.tokenizer = T5Tokenizer.from_pretrained(
                "t5-base",
                model_max_length=512  # Explicit max length to avoid warnings
            )
            logger.info("T5Tokenizer loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading T5Tokenizer: {e}")
            raise
    return get_tokenizer.tokenizer

def get_summarizer():
    if not hasattr(get_summarizer, "summarizer"):
        try:
            tokenizer = get_tokenizer()
            device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
            get_summarizer.summarizer = pipeline(
                "summarization",
                model="t5-base",
                tokenizer=tokenizer,
                framework="pt",  # Use PyTorch for better performance
                device=device,
                batch_size=BATCH_SIZE  # Configurable via environment variable
            )
            logger.info(f"Summarizer pipeline initialized on device {device}.")
        except Exception as e:
            logger.error(f"Error initializing summarizer pipeline: {e}")
            raise
    return get_summarizer.summarizer

async def summarize_text_async(text: str) -> str:
    """
    Asynchronously summarizes the input text using the T5-base model.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: The summarized text.
    """
    loop = asyncio.get_running_loop()
    try:
        summary = await loop.run_in_executor(executor, summarize_text_sync, text)
        return summary
    except Exception as e:
        logger.error(f"Error in asynchronous summarization: {e}")
        return "An error occurred during summarization."

def summarize_text_sync(text: str) -> str:
    """
    Synchronously summarizes the input text using the T5-base model by splitting it into manageable chunks.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: The combined summary of all chunks.
    """
    try:
        tokenizer = get_tokenizer()
        summarizer = get_summarizer()

        max_model_length = tokenizer.model_max_length  # 512 tokens for T5-base
        max_summary_length = 250  # Maximum tokens for the summary
        min_summary_length = 50  # Minimum tokens for the summary

        # Split text into sentences using NLTK's sentence tokenizer for accuracy
        sentences = nltk.sent_tokenize(text)

        # Encode sentences to get token counts
        encoded_sentences = [tokenizer.encode(sentence, add_special_tokens=False) for sentence in sentences]
        sentence_lengths = [len(tokens) for tokens in encoded_sentences]

        # Build chunks ensuring token counts are within the model's limit
        chunks: List[str] = []
        current_chunk = []
        current_length = 0

        for sentence, length in zip(sentences, sentence_lengths):
            if current_length + length > max_model_length:
                if current_chunk:
                    # Append the current chunk to chunks
                    chunks.append(' '.join(current_chunk))
                    # Start a new chunk with the current sentence
                    current_chunk = [sentence]
                    current_length = length
                else:
                    # If a single sentence exceeds the max length, truncate it
                    truncated_tokens = encoded_sentences[sentences.index(sentence)][:max_model_length]
                    truncated_text = tokenizer.decode(truncated_tokens, skip_special_tokens=True)
                    chunks.append(truncated_text)
                    current_chunk = []
                    current_length = 0
            else:
                # Add the sentence to the current chunk
                current_chunk.append(sentence)
                current_length += length

        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        # Filter out chunks that are too short to summarize
        valid_chunks = [chunk for chunk in chunks if len(tokenizer.encode(chunk)) >= 50]
        short_chunks = [chunk for chunk in chunks if len(tokenizer.encode(chunk)) < 50]

        # Log short chunks
        if short_chunks:
            for idx, chunk in enumerate(short_chunks):
                logger.info(f"Chunk {idx + 1}: Text is too short to summarize.")

        # Summarize valid chunks in batch
        if not valid_chunks:
            return "Text is too short to summarize."

        try:
            summaries = summarizer(
                valid_chunks,
                max_length=max_summary_length,
                min_length=min_summary_length,
                do_sample=False
            )
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            return "Error during summarization."

        # Extract summary texts
        summary_texts = [summary['summary_text'] for summary in summaries]

        # Combine summaries
        combined_summary = ' '.join(summary_texts)
        return combined_summary
    except Exception as e:
        logger.error(f"Error in summarize_text_sync: {e}")
        return "An error occurred during summarization."

