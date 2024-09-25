from transformers import pipeline

summarizer = pipeline("summarization", model="t5-base")

def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']
