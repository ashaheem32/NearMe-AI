# utils/helpers.py

import re

def clean_text(text):
    """Remove extra spaces and line breaks for better LLM prompts."""
    return re.sub(r'\s+', ' ', text).strip()

def truncate(text, max_len=500):
    """Shorten a string safely for LLM context windows."""
    return text if len(text) <= max_len else text[:max_len] + '...'

def format_score(score):
    """Format the score for display."""
    return f"{score}/10"

def safe_get(dictionary, key, default=""):
    """Safely get a value from a dict."""
    return dictionary.get(key, default)