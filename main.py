"""Main entry point for the Study Materials MCP Server."""

from __future__ import annotations

import asyncio
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import BaseModel

from services.study_material_service import StudyMaterialService
from models.result import ToolResult, ErrorInfo
from utils import errors
from settings import MATERIALS_DIR, CACHE_DIR

# Load environment configuration
load_dotenv()

# Initialize MCP server
mcp = FastMCP("study-materials-mcp")

# Initialize service
service = StudyMaterialService(materials_dir=MATERIALS_DIR, cache_dir=CACHE_DIR)


# Validation Models
class SearchMaterialIn(BaseModel):
    """Input for search_material tool."""
    query: str
    top_k: int = 5


class ExplainTopicIn(BaseModel):
    """Input for explain_topic tool."""
    topic: str


class CompareTopicsIn(BaseModel):
    """Input for compare_topics tool."""
    topic1: str
    topic2: str


class FindKnowledgeGapsIn(BaseModel):
    """Input for find_knowledge_gaps tool."""
    query: str


class RankDocumentsIn(BaseModel):
    """Input for rank_documents tool."""
    topic: str = ""


# Tool Definitions

@mcp.tool(description="""
Search study materials using semantic and keyword matching.

Use when:
- You need to find relevant study materials on a specific topic.
- You want to discover resources related to a query.

Inputs:
- query: search query (required)
- top_k: number of results to return (1-20, default: 5)

Returns (ToolResult):
- ok=true: data.results contains matching documents with relevance scores and snippets
- ok=false: error.code/message with details
""")
async def search_material(query: str, top_k: int = 5) -> dict:
    """Search study materials."""
    _ = SearchMaterialIn(query=query, top_k=top_k)  # validation
    res = await asyncio.to_thread(service.search_material, query, top_k)
    return res.to_dict()


@mcp.tool(description="""
Generate explanation of a topic from study materials.

Use when:
- You need a comprehensive explanation of a topic.
- You want to understand a concept based on available materials.

Inputs:
- topic: topic to explain (required)

Returns (ToolResult):
- ok=true: data.explanation contains formatted explanation with sources
- ok=false: error.code/message with details
""")
async def explain_topic(topic: str) -> dict:
    """Generate topic explanation."""
    _ = ExplainTopicIn(topic=topic)  # validation
    res = await asyncio.to_thread(service.explain_topic, topic)
    return res.to_dict()


@mcp.tool(description="""
Compare two topics based on available materials.

Use when:
- You want to understand similarities and differences between two topics.
- You need comparative analysis of concepts.

Inputs:
- topic1: first topic (required)
- topic2: second topic (required)

Returns (ToolResult):
- ok=true: data contains similarities, differences, and common sources
- ok=false: error.code/message with details
""")
async def compare_topics(topic1: str, topic2: str) -> dict:
    """Compare two topics."""
    _ = CompareTopicsIn(topic1=topic1, topic2=topic2)  # validation
    res = await asyncio.to_thread(service.compare_topics, topic1, topic2)
    return res.to_dict()


@mcp.tool(description="""
List all recognized topics in study materials.

Use when:
- You want to discover what topics are available in the materials.
- You need to see all covered subject areas.

Returns (ToolResult):
- ok=true: data.topics contains list of recognized topics
- ok=false: error.code/message with details
""")
async def list_topics() -> dict:
    """List all recognized topics."""
    res = await asyncio.to_thread(service.list_topics)
    return res.to_dict()


@mcp.tool(description="""
Analyze gaps in knowledge based on available materials.

Use when:
- You want to identify what information is missing for a topic.
- You need recommendations on what materials to add.

Inputs:
- query: topic to analyze (required)

Returns (ToolResult):
- ok=true: data contains gaps_identified, recommendations, and suggested_additions
- ok=false: error.code/message with details
""")
async def find_knowledge_gaps(query: str) -> dict:
    """Find knowledge gaps."""
    _ = FindKnowledgeGapsIn(query=query)  # validation
    res = await asyncio.to_thread(service.find_knowledge_gaps, query)
    return res.to_dict()


@mcp.tool(description="""
Categorize documents by topic and subtopic.

Use when:
- You want to organize documents by subject matter.
- You need to see document categorization structure.

Returns (ToolResult):
- ok=true: data.categorization contains topic-based document organization
- ok=false: error.code/message with details
""")
async def categorize_documents() -> dict:
    """Categorize documents by topic."""
    res = await asyncio.to_thread(service.categorize_documents_by_topic)
    return res.to_dict()


@mcp.tool(description="""
Rank documents by importance score.

Use when:
- You want to prioritize which documents to read first.
- You need to identify most important materials for a topic.

Inputs:
- topic: optional topic filter

Returns (ToolResult):
- ok=true: data.ranked_documents contains documents sorted by importance
- ok=false: error.code/message with details
""")
async def rank_documents(topic: str = "") -> dict:
    """Rank documents by importance."""
    _ = RankDocumentsIn(topic=topic)  # validation
    res = await asyncio.to_thread(service.rank_documents_by_importance, topic)
    return res.to_dict()


if __name__ == "__main__":
    mcp.run()
