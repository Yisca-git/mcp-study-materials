from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class DocumentChunk:
    """Represents a chunk of a document."""
    id: str
    filename: str
    content: str
    chunk_index: int
    embedding: Optional[list[float]] = None
    topic: Optional[str] = None
    subtopic: Optional[str] = None
    importance_score: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "content": self.content[:500] + "..." if len(self.content) > 500 else self.content,
            "chunk_index": self.chunk_index,
            "topic": self.topic,
            "subtopic": self.subtopic,
            "importance_score": self.importance_score,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class Document:
    """Represents a study document."""
    filename: str
    filepath: str
    content: str
    chunks: list[DocumentChunk] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    importance_score: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "filepath": self.filepath,
            "chunk_count": len(self.chunks),
            "topics": self.topics,
            "importance_score": self.importance_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class SearchResult:
    """Represents a search result."""
    filename: str
    relevance_score: float
    snippets: list[str]
    topic: Optional[str] = None
    confidence: float = 0.0
    
    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "relevance_score": self.relevance_score,
            "snippets": self.snippets,
            "topic": self.topic,
            "confidence": self.confidence
        }


@dataclass
class TopicInfo:
    """Information about a topic."""
    name: str
    description: str = ""
    subtopics: list[str] = field(default_factory=list)
    document_count: int = 0
    related_topics: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "subtopics": self.subtopics,
            "document_count": self.document_count,
            "related_topics": self.related_topics
        }
