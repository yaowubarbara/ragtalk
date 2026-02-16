import re


def chunk_document(text: str, doc_type: str, max_chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into semantic chunks based on document type.

    - Quotes: keep as-is (don't split)
    - Long paragraphs: split by sentences, merge into chunks up to max_chunk_size
    - Short text: keep as-is
    """
    if doc_type == "quote":
        # Quotes should stay intact
        return [text] if text else []

    if len(text) <= max_chunk_size:
        return [text] if text else []

    # Split long text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if not sentence.strip():
            continue

        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk = f"{current_chunk} {sentence}".strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            # If a single sentence exceeds max, include it anyway
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
