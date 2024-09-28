from transformers import pipeline, T5Tokenizer
import logging
import torch
import nltk
from typing import List

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download NLTK data for sentence tokenization if not already present
nltk.download('punkt', quiet=True)

# Initialize the tokenizer with explicit max length to avoid warnings
tokenizer = T5Tokenizer.from_pretrained("t5-base", model_max_length=512)

# Initialize the summarizer pipeline with PyTorch framework and GPU if available
device = 0 if torch.cuda.is_available() else -1  # Use GPU (0) if available, else CPU (-1)
summarizer = pipeline(
    "summarization",
    model="t5-base",
    tokenizer=tokenizer,
    framework="pt",  # Use "pt" for PyTorch, generally faster and more efficient
    device=device,
    batch_size=8  # Adjust based on your GPU memory; higher for more parallelism
)

def summarize_text(text: str) -> str:
    """
    Summarizes the input text using the T5-base model by splitting it into manageable chunks.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: The combined summary of all chunks.
    """
    max_model_length = tokenizer.model_max_length  # 512 tokens for T5-base
    max_summary_length = 150  # Maximum tokens for the summary
    min_summary_length = 40   # Minimum tokens for the summary

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
