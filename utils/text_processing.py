"""Text processing utilities."""

import re
from typing import Optional


def extract_snippets(content: str, query: str, max_snippets: int = 3, context_lines: int = 1) -> list[str]:
    """Extract relevant snippets from content around query matches."""
    snippets = []
    query_lower = query.lower()
    lines = content.split('\n')
    
    seen_snippets = set()
    
    for i, line in enumerate(lines):
        if query_lower in line.lower():
            # Include context (previous and next lines)
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            snippet = ' '.join(lines[start:end]).strip()
            
            # Ensure snippet is meaningful and not a duplicate
            if snippet and len(snippet) > 20 and snippet not in seen_snippets:
                snippets.append(snippet)
                seen_snippets.add(snippet)
                
                if len(snippets) >= max_snippets:
                    break
    
    return snippets


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    sentences = text.split('.')
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Add period back
        sentence_with_period = sentence + "."
        
        if len(current_chunk) + len(sentence_with_period) <= chunk_size:
            current_chunk += " " + sentence_with_period if current_chunk else sentence_with_period
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
                # Create overlap by repeating last part of previous chunk
                current_chunk = current_chunk[-overlap:] + " " + sentence_with_period
            else:
                chunks.append(sentence_with_period)
                current_chunk = ""
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def extract_keywords(text: str, num_keywords: int = 10) -> list[str]:
    """Extract keywords from text using simple frequency analysis."""
    # Remove common stopwords
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who',
        'when', 'where', 'why', 'how', 'as', 'if', 'from', 'up', 'out', 'so'
    }
    
    # Extract words
    words = re.findall(r'\b[a-z]+\b', text.lower())
    
    # Count frequency
    word_freq = {}
    for word in words:
        if word not in stopwords and len(word) > 3:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return [word for word, _ in sorted_words[:num_keywords]]


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity based on common words."""
    words1 = set(extract_keywords(text1, 100))
    words2 = set(extract_keywords(text2, 100))
    
    if not words1 or not words2:
        return 0.0
    
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
