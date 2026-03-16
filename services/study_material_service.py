"""Core service for study material management."""

from __future__ import annotations

import os
import json
from datetime import datetime
from typing import Optional

from models.result import ToolResult, ErrorInfo
from models.study_material_models import SearchResult
from utils import errors
from utils.paths import abspath, ensure_dir_exists
from utils.validate import validate_query, validate_topic, validate_topics, validate_materials_dir
from utils.text_processing import extract_snippets, extract_keywords, truncate_text, calculate_text_similarity
from services.document_processor import DocumentProcessor


class StudyMaterialService:
    """Service for managing and searching study materials."""
    
    def __init__(self, materials_dir: str = "study_materials", cache_dir: str = "cache"):
        self.materials_dir = abspath(materials_dir)
        self.cache_dir = abspath(cache_dir)
        self.processor = DocumentProcessor(materials_dir, cache_dir)
        
        ensure_dir_exists(self.materials_dir)
        ensure_dir_exists(self.cache_dir)
        
        self.embeddings_cache_file = os.path.join(self.cache_dir, "embeddings_cache.json")
        self.topics_file = os.path.join(self.cache_dir, "topics.json")
        self.documents_cache_file = os.path.join(self.cache_dir, "documents_cache.json")
        
        # In-memory stores
        self.documents = {}
        self.embeddings = {}
        self.topics = {}
        self.document_index = {}  # Maps filenames to their content
        
        self._load_cache()
        self._index_materials()
    
    def _load_cache(self) -> None:
        """Load cached data."""
        try:
            if os.path.exists(self.embeddings_cache_file):
                with open(self.embeddings_cache_file, 'r') as f:
                    self.embeddings = json.load(f)
        except Exception:
            pass
        
        try:
            if os.path.exists(self.topics_file):
                with open(self.topics_file, 'r') as f:
                    self.topics = json.load(f)
        except Exception:
            pass
    
    def _save_cache(self) -> None:
        """Save cache to disk."""
        try:
            with open(self.embeddings_cache_file, 'w') as f:
                json.dump(self.embeddings, f, indent=2)
            with open(self.topics_file, 'w') as f:
                json.dump(self.topics, f, indent=2)
        except Exception:
            pass
    
    def _index_materials(self) -> None:
        """Index all materials in the directory."""
        self.document_index = {}
        
        if not os.path.isdir(self.materials_dir):
            return
        
        for filename in os.listdir(self.materials_dir):
            filepath = os.path.join(self.materials_dir, filename)
            if not os.path.isfile(filepath):
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self.document_index[filename] = content
            except Exception:
                continue
    
    def search_material(self, query: str, top_k: int = 5) -> ToolResult:
        """Search study materials using keyword and semantic matching."""
        if not validate_query(query):
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=errors.INVALID_QUERY,
                    message="Query cannot be empty.",
                    details={"query": query}
                )
            )
        
        if not self.document_index:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=errors.EMPTY_MATERIALS,
                    message="No study materials found.",
                    details={}
                )
            )
        
        results = []
        query_lower = query.lower()
        query_keywords = set(extract_keywords(query, num_keywords=5))
        
        for filename, content in self.document_index.items():
            # Keyword matching score
            keyword_score = 0.0
            for keyword in query_keywords:
                if keyword in content.lower():
                    keyword_score += content.lower().count(keyword) * 0.1
            
            # Direct query matching
            if query_lower in content.lower():
                keyword_score += 5.0
            
            # Text similarity score
            content_keywords = set(extract_keywords(content, num_keywords=20))
            similarity = calculate_text_similarity(query, content)
            
            combined_score = keyword_score + (similarity * 3.0)
            
            # Extract snippets
            snippets = extract_snippets(content, query, max_snippets=3)
            
            if combined_score > 0 or snippets:
                results.append(SearchResult(
                    filename=filename,
                    relevance_score=combined_score,
                    snippets=snippets,
                    confidence=min(0.95, combined_score / 10.0)
                ))
        
        # Sort by relevance
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        results = results[:top_k]
        
        if not results:
            return ToolResult(
                ok=True,
                data={
                    "query": query,
                    "results_count": 0,
                    "results": [],
                    "confidence": 0.0,
                    "message": "No matching materials found."
                }
            )
        
        return ToolResult(
            ok=True,
            data={
                "query": query,
                "results_count": len(results),
                "results": [r.to_dict() for r in results],
                "confidence": results[0].confidence if results else 0.0
            }
        )
    
    def explain_topic(self, topic: str) -> ToolResult:
        """Generate explanation of a topic from materials."""
        if not validate_topic(topic):
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=errors.INVALID_TOPIC,
                    message="Topic cannot be empty.",
                    details={"topic": topic}
                )
            )
        
        # Search for topic
        search_result = self.search_material(topic, top_k=10)
        if not search_result.ok:
            return search_result
        
        results_data = search_result.data.get("results", [])
        
        if not results_data:
            return ToolResult(
                ok=True,
                data={
                    "topic": topic,
                    "explanation": f"No specific information found about '{topic}' in study materials.",
                    "related_topics": [],
                    "source_files": [],
                    "confidence": 0.0
                }
            )
        
        # Compile explanation
        source_files = [r["filename"] for r in results_data[:3]]
        explanation = f"# {topic}\n\nBased on available study materials:\n\n"
        
        for i, result in enumerate(results_data[:3], 1):
            explanation += f"## Source {i}: {result['filename']}\n"
            for snippet in result.get("snippets", [])[:2]:
                explanation += f"- {truncate_text(snippet, max_length=300)}\n"
            explanation += "\n"
        
        related_topics = self._find_related_topics(topic)
        
        return ToolResult(
            ok=True,
            data={
                "topic": topic,
                "explanation": explanation,
                "related_topics": related_topics,
                "source_files": source_files,
                "confidence": min(0.95, len(results_data) * 0.15)
            }
        )
    
    def compare_topics(self, topic1: str, topic2: str) -> ToolResult:
        """Compare two topics based on materials."""
        if not validate_topics(topic1, topic2):
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=errors.INVALID_TOPICS,
                    message="Both topics must be provided and non-empty.",
                    details={"topic1": topic1, "topic2": topic2}
                )
            )
        
        # Get explanations for both
        exp1 = self.explain_topic(topic1)
        exp2 = self.explain_topic(topic2)
        
        if not exp1.ok or not exp2.ok:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=errors.COMPARISON_FAILED,
                    message="Could not retrieve information for comparison.",
                    details={"topic1": topic1, "topic2": topic2}
                )
            )
        
        # Extract and compare
        data1 = exp1.data
        data2 = exp2.data
        
        similarities = [
            "Both are fundamental concepts in their domains",
            "Both require understanding of core principles"
        ]
        
        # Add more sophisticated comparison
        source_files1 = set(data1.get("source_files", []))
        source_files2 = set(data2.get("source_files", []))
        common_sources = source_files1.intersection(source_files2)
        
        if common_sources:
            similarities.append(f"Both topics appear in the same materials: {', '.join(common_sources)}")
        
        all_sources = source_files1.union(source_files2)
        
        return ToolResult(
            ok=True,
            data={
                "topic1": topic1,
                "topic2": topic2,
                "similarities": similarities,
                "differences": [
                    f"{topic1} is covered in: {', '.join(source_files1) if source_files1 else 'limited materials'}",
                    f"{topic2} is covered in: {', '.join(source_files2) if source_files2 else 'limited materials'}"
                ],
                "common_materials": list(common_sources),
                "all_sources": list(all_sources),
                "confidence": (data1.get("confidence", 0) + data2.get("confidence", 0)) / 2
            }
        )
    
    def list_topics(self) -> ToolResult:
        """List all recognized topics."""
        topics_set = set()
        
        # Extract from indexed documents
        for filename, content in self.document_index.items():
            keywords = extract_keywords(content, num_keywords=3)
            topics_set.update(keywords)
        
        # Add filename-based topics
        for filename in self.document_index.keys():
            name_without_ext = os.path.splitext(filename)[0]
            topics_set.add(name_without_ext)
        
        topics_list = sorted(list(topics_set))
        
        return ToolResult(
            ok=True,
            data={
                "topics": topics_list,
                "count": len(topics_list),
                "last_updated": datetime.now().isoformat()
            }
        )
    
    def find_knowledge_gaps(self, query: str) -> ToolResult:
        """Identify knowledge gaps based on query."""
        if not validate_query(query):
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=errors.INVALID_QUERY,
                    message="Query cannot be empty.",
                    details={"query": query}
                )
            )
        
        search_result = self.search_material(query, top_k=5)
        
        if not search_result.ok:
            return search_result
        
        results = search_result.data.get("results", [])
        confidence = search_result.data.get("confidence", 0)
        
        gaps = []
        recommendations = []
        
        if not results:
            gaps.append("No materials found for this topic")
            recommendations.append("Add introductory materials on the topic")
            recommendations.append("Include references and further reading resources")
        elif confidence < 0.5:
            gaps.append("Limited coverage of this topic")
            recommendations.append("Expand with more detailed explanations")
            recommendations.append("Add practical examples and use cases")
        elif len(results) < 3:
            gaps.append("Few alternative perspectives available")
            recommendations.append("Add materials from different sources")
            recommendations.append("Include complementary viewpoints")
        else:
            gaps.append("Consider advanced topics and specializations")
            recommendations.append("Add specialized subtopics")
            recommendations.append("Include advanced tutorials and research papers")
        
        return ToolResult(
            ok=True,
            data={
                "query": query,
                "confidence_level": confidence,
                "gaps_identified": gaps,
                "recommendations": recommendations,
                "covered_materials": len(results),
                "suggested_additions": [
                    "Introductory guides",
                    "Advanced tutorials",
                    "Practical exercises",
                    "Summary documents",
                    "Real-world case studies"
                ]
            }
        )
    
    def categorize_documents_by_topic(self) -> ToolResult:
        """Categorize documents by topic and subtopic."""
        categorized = {}
        
        for filename, content in self.document_index.items():
            category = self._infer_category(filename, content)
            
            if category not in categorized:
                categorized[category] = []
            
            filepath = os.path.join(self.materials_dir, filename)
            categorized[category].append({
                "filename": filename,
                "filepath": filepath,
                "size": len(content),
                "topics": extract_keywords(content, num_keywords=3)
            })
        
        organization_plan = {}
        for category, docs in categorized.items():
            org_dir = os.path.join(self.materials_dir, category)
            organization_plan[category] = {
                "directory": org_dir,
                "document_count": len(docs),
                "documents": docs
            }
        
        return ToolResult(
            ok=True,
            data={
                "categorization": organization_plan,
                "total_documents": sum(len(docs) for docs in categorized.values()),
                "categories_count": len(categorized),
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def _infer_category(self, filename: str, content: str) -> str:
        """Infer document category from filename and content."""
        name_lower = filename.lower()
        content_lower = content.lower()
        
        categories_keywords = {
            "Mathematics": ["math", "algebra", "calculus", "geometry", "equation", "theorem"],
            "Physics": ["physics", "mechanics", "thermodynamics", "quantum", "energy"],
            "Chemistry": ["chemistry", "organic", "inorganic", "reaction", "compound"],
            "Biology": ["biology", "genetics", "ecology", "cell", "organism"],
            "Computer Science": ["programming", "algorithm", "code", "software", "data structure"],
            "History": ["history", "historical", "century", "event", "period"],
            "Literature": ["literature", "novel", "poem", "author", "story"],
            "General": []
        }
        
        for category, keywords in categories_keywords.items():
            for keyword in keywords:
                if keyword in name_lower or keyword in content_lower:
                    return category
        
        return "General"
    
    def _find_related_topics(self, topic: str) -> list[str]:
        """Find topics related to the given topic."""
        related = []
        all_topics = self.list_topics().data.get("topics", [])
        
        topic_lower = topic.lower()
        query_keywords = set(extract_keywords(topic, num_keywords=3))
        
        for t in all_topics:
            if t.lower() != topic_lower:
                t_keywords = set(extract_keywords(t, num_keywords=3))
                if query_keywords.intersection(t_keywords):
                    related.append(t)
        
        return related[:5]
    
    def rank_documents_by_importance(self, topic: str = "") -> ToolResult:
        """Rank documents by importance."""
        ranked_docs = []
        
        for filename, content in self.document_index.items():
            importance_score = self._calculate_importance(filename, content, topic)
            
            filepath = os.path.join(self.materials_dir, filename)
            ranked_docs.append({
                "filename": filename,
                "filepath": filepath,
                "importance_score": importance_score,
                "size": len(content),
                "reasons": self._importance_reasons(content, filename)
            })
        
        ranked_docs.sort(key=lambda x: x["importance_score"], reverse=True)
        
        return ToolResult(
            ok=True,
            data={
                "ranked_documents": ranked_docs,
                "total_documents": len(ranked_docs),
                "ranking_criteria": [
                    "Contains summaries and overviews",
                    "Includes practical exercises",
                    "Has important references",
                    "Document comprehensiveness",
                    "Topic relevance"
                ],
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def _calculate_importance(self, filename: str, content: str, topic: str = "") -> float:
        """Calculate importance score."""
        score = 0.5
        content_lower = content.lower()
        
        # Summary indicators
        summary_keywords = ["summary", "overview", "introduction", "conclusion", "abstract"]
        for keyword in summary_keywords:
            if keyword in content_lower:
                score += 0.1
        
        # Exercise indicators
        exercise_keywords = ["exercise", "problem", "solution", "quiz", "test", "practice"]
        for keyword in exercise_keywords:
            if keyword in content_lower:
                score += 0.15
        
        # Reference indicators
        ref_keywords = ["reference", "citation", "source", "bibliography", "reading"]
        for keyword in ref_keywords:
            if keyword in content_lower:
                score += 0.1
        
        # Content size bonus
        score += min(0.2, len(content) / 100000)
        
        # Topic match bonus
        if topic and topic.lower() in content_lower:
            score += 0.15
        
        return min(1.0, score)
    
    def _importance_reasons(self, content: str, filename: str) -> list[str]:
        """Get reasons for importance score."""
        reasons = []
        content_lower = content.lower()
        
        if any(kw in content_lower for kw in ["summary", "overview"]):
            reasons.append("Contains summary information")
        if any(kw in content_lower for kw in ["exercise", "problem", "solution"]):
            reasons.append("Includes practical exercises")
        if any(kw in content_lower for kw in ["reference", "bibliography"]):
            reasons.append("Contains important references")
        if len(content) > 50000:
            reasons.append("Comprehensive document")
        
        return reasons if reasons else ["Core material"]
