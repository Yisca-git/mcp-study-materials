"""Service for processing documents."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from models.result import ToolResult, ErrorInfo
from models.study_material_models import Document, DocumentChunk
from utils import errors
from utils.paths import abspath, is_file_readable, ensure_dir_exists, get_file_extension
from utils.text_processing import chunk_text, extract_keywords


class DocumentProcessor:
    """Processes and manages study documents."""
    
    SUPPORTED_FORMATS = ['txt', 'pdf', 'md']
    
    def __init__(self, materials_dir: str = "study_materials", cache_dir: str = "cache"):
        self.materials_dir = abspath(materials_dir)
        self.cache_dir = abspath(cache_dir)
        ensure_dir_exists(self.materials_dir)
        ensure_dir_exists(self.cache_dir)
    
    def load_document(self, filename: str) -> ToolResult:
        """Load and process a document from materials directory."""
        filepath = os.path.join(self.materials_dir, filename)
        
        if not is_file_readable(filepath):
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=errors.FILE_NOT_FOUND,
                    message=f"File not found or not readable: {filename}",
                    details={"filename": filename, "filepath": filepath}
                )
            )
        
        # Check file format
        ext = get_file_extension(filename)
        if ext not in self.SUPPORTED_FORMATS:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=errors.INVALID_FILE_FORMAT,
                    message=f"Unsupported file format: {ext}",
                    details={"filename": filename, "supported": self.SUPPORTED_FORMATS}
                )
            )
        
        try:
            # Read file content
            content = self._read_file(filepath)
            
            # Create document
            document = Document(
                filename=filename,
                filepath=filepath,
                content=content
            )
            
            # Extract topics and keywords
            keywords = extract_keywords(content, num_keywords=5)
            document.topics = keywords
            
            # Create chunks
            chunks_list = chunk_text(content, chunk_size=500, overlap=50)
            for idx, chunk_content in enumerate(chunks_list):
                chunk = DocumentChunk(
                    id=f"{filename}_chunk_{idx}",
                    filename=filename,
                    content=chunk_content,
                    chunk_index=idx,
                    topic=keywords[0] if keywords else "General"
                )
                document.chunks.append(chunk)
            
            return ToolResult(
                ok=True,
                data={
                    "filename": filename,
                    "chunk_count": len(document.chunks),
                    "topics": document.topics,
                    "content_length": len(content)
                }
            )
        
        except Exception as e:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=errors.DOCUMENT_PROCESSING_FAILED,
                    message="Failed to process document",
                    details={"filename": filename, "error": str(e)}
                )
            )
    
    def _read_file(self, filepath: str) -> str:
        """Read file content based on format."""
        ext = get_file_extension(filepath).lower()
        
        if ext == 'pdf':
            return self._read_pdf(filepath)
        elif ext in ['txt', 'md']:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported format: {ext}")
    
    def _read_pdf(self, filepath: str) -> str:
        """Read PDF file (simplified - requires PyPDF2 or similar)."""
        try:
            # Try to use PyPDF2 if available, otherwise return placeholder
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(filepath)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except ImportError:
                # Fallback: return simple text indicating PDF processing
                return f"[PDF Document: {os.path.basename(filepath)}]\nPDF processing requires PyPDF2 library."
        except Exception as e:
            raise ValueError(f"Failed to read PDF: {e}")
    
    def list_documents(self) -> ToolResult:
        """List all documents in materials directory."""
        try:
            documents = []
            
            for filename in os.listdir(self.materials_dir):
                filepath = os.path.join(self.materials_dir, filename)
                
                if not os.path.isfile(filepath):
                    continue
                
                ext = get_file_extension(filename)
                if ext not in self.SUPPORTED_FORMATS:
                    continue
                
                file_size = os.path.getsize(filepath)
                documents.append({
                    "filename": filename,
                    "size": file_size,
                    "format": ext
                })
            
            return ToolResult(
                ok=True,
                data={
                    "documents": documents,
                    "count": len(documents)
                }
            )
        
        except Exception as e:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=errors.INTERNAL_ERROR,
                    message="Failed to list documents",
                    details={"error": str(e)}
                )
            )
