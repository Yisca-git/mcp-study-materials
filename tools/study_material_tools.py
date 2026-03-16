"""MCP tools for study material operations."""

from __future__ import annotations

from typing import Any

from services.study_material_service import StudyMaterialService
from models.result import ToolResult


class StudyMaterialTools:
    """MCP Tools for study material interaction."""
    
    def __init__(self, materials_dir: str = "study_materials", cache_dir: str = "cache"):
        self.service = StudyMaterialService(materials_dir, cache_dir)
    
    def search_material(self, **kwargs) -> dict[str, Any]:
        """Search study materials by semantic and keyword matching."""
        query = kwargs.get("query", "")
        top_k = kwargs.get("top_k", 5)
        
        result = self.service.search_material(query, top_k=top_k)
        return self._format_response(result)
    
    def explain_topic(self, **kwargs) -> dict[str, Any]:
        """Generate explanation of a topic from materials."""
        topic = kwargs.get("topic", "")
        
        result = self.service.explain_topic(topic)
        return self._format_response(result)
    
    def compare_topics(self, **kwargs) -> dict[str, Any]:
        """Compare two topics based on available materials."""
        topic1 = kwargs.get("topic1", "")
        topic2 = kwargs.get("topic2", "")
        
        result = self.service.compare_topics(topic1, topic2)
        return self._format_response(result)
    
    def list_topics(self, **kwargs) -> dict[str, Any]:
        """List all recognized topics in study materials."""
        result = self.service.list_topics()
        return self._format_response(result)
    
    def find_knowledge_gaps(self, **kwargs) -> dict[str, Any]:
        """Analyze gaps in knowledge based on available materials."""
        query = kwargs.get("query", "")
        
        result = self.service.find_knowledge_gaps(query)
        return self._format_response(result)
    
    def categorize_documents(self, **kwargs) -> dict[str, Any]:
        """Categorize documents by topic and subtopic."""
        result = self.service.categorize_documents_by_topic()
        return self._format_response(result)
    
    def rank_documents(self, **kwargs) -> dict[str, Any]:
        """Rank documents by importance score."""
        topic = kwargs.get("topic", "")
        
        result = self.service.rank_documents_by_importance(topic)
        return self._format_response(result)
    
    def _format_response(self, result: ToolResult) -> dict[str, Any]:
        """Format ToolResult to response dictionary."""
        if result.ok:
            return {
                "success": True,
                "data": result.data
            }
        else:
            return {
                "success": False,
                "error": {
                    "code": result.error.code if result.error else "UNKNOWN",
                    "message": result.error.message if result.error else "Unknown error",
                    "hint": result.error.hint if result.error else None,
                    "details": result.error.details if result.error else {}
                }
            }
