from transformers import pipeline
import logging

summarizer = pipeline("summarization", model="t5-base")

def summarize_text(text: str) -> str:
    max_tokens = 512  # Model's max sequence length
    tokenizer = summarizer.tokenizer

    # Split text into chunks
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        token_length = len(tokenizer.encode(word, add_special_tokens=False))
        if current_length + token_length > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = token_length
        else:
            current_chunk.append(word)
            current_length += token_length

    # Add the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    # Summarize each chunk
    summaries = []
    for chunk in chunks:
        if len(chunk) < 50:
            summaries.append("Text is too short to summarize.")
        else:
            summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
            summaries.append(summary[0]['summary_text'])

    # Combine summaries
    combined_summary = ' '.join(summaries)
    return combined_summary
