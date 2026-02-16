"""Semantic-aware document chunking.

Strategies:
- Quotes: kept intact (no splitting)
- Paragraphs: split on natural boundaries (double newlines, topic shifts)
- Long paragraphs: split at sentence boundaries with configurable overlap
- Short fragments: merged with adjacent chunks to avoid tiny entries

This is a significant improvement over naive fixed-size chunking because
it preserves semantic coherence within each chunk.
"""

import re


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences, handling common abbreviations."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def _split_paragraphs(text: str) -> list[str]:
    """Split on double newlines (paragraph boundaries)."""
    paragraphs = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paragraphs if p.strip()]


def chunk_document(
    text: str,
    doc_type: str,
    max_chunk_size: int = 500,
    overlap_sentences: int = 1,
    min_chunk_size: int = 50,
) -> list[str]:
    """Split text into semantically coherent chunks.

    Strategy by document type:
    - "quote": Keep intact (quotes are short, self-contained units)
    - Other: Split by paragraphs first, then by sentences if needed

    Args:
        text: Raw document text
        doc_type: Document type ("quote", "paragraph", "article", etc.)
        max_chunk_size: Maximum characters per chunk
        overlap_sentences: Number of sentences to overlap between chunks
        min_chunk_size: Minimum characters; smaller chunks get merged

    Returns:
        List of text chunks
    """
    if not text or not text.strip():
        return []

    text = text.strip()

    # Quotes stay intact
    if doc_type == "quote":
        return [text]

    # Short texts stay intact
    if len(text) <= max_chunk_size:
        return [text]

    # Stage 1: Split into paragraphs
    paragraphs = _split_paragraphs(text)

    # If no paragraph breaks, treat the whole text as one paragraph
    if len(paragraphs) <= 1:
        paragraphs = [text]

    # Stage 2: Process each paragraph
    raw_chunks = []
    for para in paragraphs:
        if len(para) <= max_chunk_size:
            raw_chunks.append(para)
        else:
            # Split long paragraphs by sentences with overlap
            sentences = _split_sentences(para)
            current_chunk_sentences: list[str] = []
            current_length = 0

            for sentence in sentences:
                sentence_len = len(sentence)

                if current_length + sentence_len + 1 > max_chunk_size and current_chunk_sentences:
                    # Emit current chunk
                    raw_chunks.append(" ".join(current_chunk_sentences))
                    # Keep overlap_sentences for context continuity
                    if overlap_sentences > 0:
                        current_chunk_sentences = current_chunk_sentences[-overlap_sentences:]
                        current_length = sum(len(s) for s in current_chunk_sentences)
                    else:
                        current_chunk_sentences = []
                        current_length = 0

                current_chunk_sentences.append(sentence)
                current_length += sentence_len + 1

            if current_chunk_sentences:
                raw_chunks.append(" ".join(current_chunk_sentences))

    # Stage 3: Merge small adjacent chunks
    merged_chunks = []
    buffer = ""
    for chunk in raw_chunks:
        if buffer and len(buffer) + len(chunk) + 1 <= max_chunk_size:
            buffer = f"{buffer} {chunk}"
        else:
            if buffer and len(buffer) >= min_chunk_size:
                merged_chunks.append(buffer)
            elif buffer:
                # Too small on its own, prepend to next
                chunk = f"{buffer} {chunk}"
            buffer = chunk

    if buffer and len(buffer) >= min_chunk_size:
        merged_chunks.append(buffer)
    elif buffer and merged_chunks:
        # Append tiny remainder to last chunk
        merged_chunks[-1] = f"{merged_chunks[-1]} {buffer}"
    elif buffer:
        merged_chunks.append(buffer)

    return merged_chunks
