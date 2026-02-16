import re


def clean_text(text: str) -> str:
    """Clean raw scraped text: remove HTML artifacts, normalize whitespace, etc."""
    # Remove any remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Normalize unicode quotes and dashes
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def is_useful(text: str, min_length: int = 30) -> bool:
    """Filter out overly short or boilerplate text."""
    if len(text) < min_length:
        return False
    # Skip navigation/boilerplate patterns
    boilerplate = [
        "click here", "subscribe", "cookie", "privacy policy",
        "terms of service", "all rights reserved", "copyright",
    ]
    lower = text.lower()
    return not any(bp in lower for bp in boilerplate)
