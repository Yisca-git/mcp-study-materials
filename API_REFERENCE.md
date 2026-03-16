# Study Materials MCP Server - API Reference

## Base Response Format

All API responses follow this structure:

### Success Response
```json
{
  "success": true,
  "data": {
    "key": "value",
    ...
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "hint": "Suggested resolution (optional)",
    "details": {
      "contextual": "information"
    }
  }
}
```

---

## Tool: search_material

Search study materials using keyword and semantic matching.

### Request
```json
{
  "query": "string",
  "top_k": 5
}
```

**Parameters:**
- `query` (required, string): Search query
- `top_k` (optional, integer): Number of results (1-20, default: 5)

### Response
```json
{
  "success": true,
  "data": {
    "query": "What is algebra?",
    "results_count": 3,
    "confidence": 0.95,
    "results": [
      {
        "filename": "algebra_basics.txt",
        "relevance_score": 10.5,
        "snippets": [
          "Algebra is a branch of mathematics...",
          "Variables are symbols representing..."
        ],
        "topic": "Mathematics",
        "confidence": 0.95
      }
    ]
  }
}
```

**Response Fields:**
- `query`: The search query used
- `results_count`: Number of results returned
- `confidence`: Overall confidence in results (0.0-1.0)
- `results`: Array of search results

**Result Fields:**
- `filename`: Source document name
- `relevance_score`: Numerical relevance score
- `snippets`: Text snippets around query matches
- `topic`: Inferred topic (optional)
- `confidence`: Result confidence (0.0-1.0)

### Examples

**Example 1: Basic Search**
```python
request = {
  "query": "linear equations"
}
```

**Example 2: Specific Number of Results**
```python
request = {
  "query": "quadratic formula",
  "top_k": 10
}
```

---

## Tool: explain_topic

Generate a comprehensive explanation of a topic from available materials.

### Request
```json
{
  "topic": "string"
}
```

**Parameters:**
- `topic` (required, string): Topic to explain

### Response
```json
{
  "success": true,
  "data": {
    "topic": "Algebra",
    "explanation": "# Algebra\n\nBased on available study materials:\n\n## Source 1: algebra_basics.txt\n- Algebra is a branch of mathematics...\n- Variables are symbols representing...",
    "related_topics": ["Variables", "Equations", "Functions"],
    "source_files": ["algebra_basics.txt", "intro_math.txt"],
    "confidence": 0.85
  }
}
```

**Response Fields:**
- `topic`: The topic explained
- `explanation`: Formatted explanation with references
- `related_topics`: List of semantically related topics
- `source_files`: Documents used in explanation
- `confidence`: Confidence in explanation (0.0-1.0)

### Examples

**Example 1: Single Word Topic**
```python
request = {
  "topic": "Calculus"
}
```

**Example 2: Multi-Word Topic**
```python
request = {
  "topic": "Differential Equations"
}
```

---

## Tool: compare_topics

Compare two topics and highlight similarities and differences.

### Request
```json
{
  "topic1": "string",
  "topic2": "string"
}
```

**Parameters:**
- `topic1` (required, string): First topic
- `topic2` (required, string): Second topic

### Response
```json
{
  "success": true,
  "data": {
    "topic1": "Algebra",
    "topic2": "Geometry",
    "similarities": [
      "Both are foundational mathematical concepts",
      "Both covered in materials on Abstract Math"
    ],
    "differences": [
      "Algebra is covered in 3 documents",
      "Geometry is covered in 2 documents"
    ],
    "common_materials": ["intro_math.txt"],
    "all_sources": ["algebra_basics.txt", "geometry.txt", "intro_math.txt"],
    "confidence": 0.80
  }
}
```

**Response Fields:**
- `topic1`: First topic
- `topic2`: Second topic
- `similarities`: List of similarities
- `differences`: List of differences
- `common_materials`: Documents covering both topics
- `all_sources`: All documents for either topic
- `confidence`: Average confidence (0.0-1.0)

### Examples

**Example 1: Basic Comparison**
```python
request = {
  "topic1": "Sine",
  "topic2": "Cosine"
}
```

**Example 2: Different Domains**
```python
request = {
  "topic1": "Photosynthesis",
  "topic2": "Respiration"
}
```

---

## Tool: list_topics

List all recognized topics in the study materials.

### Request
```json
{}
```

No parameters required.

### Response
```json
{
  "success": true,
  "data": {
    "topics": [
      "Algebra",
      "Calculus",
      "Geometry",
      "Functions",
      "Trigonometry"
    ],
    "count": 5,
    "last_updated": "2024-01-15T10:30:45.123456"
  }
}
```

**Response Fields:**
- `topics`: List of recognized topics
- `count`: Number of topics
- `last_updated`: ISO timestamp of last update

### Examples

**Example 1: Get All Topics**
```python
request = {}
```

---

## Tool: find_knowledge_gaps

Analyze what information is missing for a given topic.

### Request
```json
{
  "query": "string"
}
```

**Parameters:**
- `query` (required, string): Topic to analyze

### Response
```json
{
  "success": true,
  "data": {
    "query": "Advanced Calculus",
    "confidence_level": 0.45,
    "gaps_identified": [
      "Limited coverage of this topic",
      "Few alternative perspectives available"
    ],
    "recommendations": [
      "Expand with more detailed explanations",
      "Add materials from different sources",
      "Include complementary viewpoints"
    ],
    "covered_materials": 2,
    "suggested_additions": [
      "Introductory guides",
      "Advanced tutorials",
      "Practical exercises",
      "Summary documents",
      "Real-world case studies"
    ]
  }
}
```

**Response Fields:**
- `query`: Topic analyzed
- `confidence_level`: Confidence in current coverage (0.0-1.0)
- `gaps_identified`: List of identified gaps
- `recommendations`: Suggested improvements
- `covered_materials`: Number of documents covering topic
- `suggested_additions`: Types of materials to add

### Examples

**Example 1: Check Gap Analysis**
```python
request = {
  "query": "Machine Learning"
}
```

---

## Tool: categorize_documents

Automatically categorize documents by subject matter.

### Request
```json
{}
```

No parameters required.

### Response
```json
{
  "success": true,
  "data": {
    "categorization": {
      "Mathematics": {
        "directory": "study_materials/Mathematics",
        "document_count": 5,
        "documents": [
          {
            "filename": "algebra_basics.txt",
            "filepath": "study_materials/algebra_basics.txt",
            "size": 2500,
            "topics": ["Algebra", "Variables", "Equations"]
          }
        ]
      },
      "Physics": {
        "directory": "study_materials/Physics",
        "document_count": 3,
        "documents": []
      }
    },
    "total_documents": 8,
    "categories_count": 2,
    "timestamp": "2024-01-15T10:30:45.123456"
  }
}
```

**Response Fields:**
- `categorization`: Mapping of categories to document lists
- `total_documents`: Total number of documents
- `categories_count`: Number of categories found
- `timestamp`: When categorization was performed

**Document Fields:**
- `filename`: Document file name
- `filepath`: Full path to document
- `size`: Document size in bytes/characters
- `topics`: Extracted topics from document

### Examples

**Example 1: Categorize All**
```python
request = {}
```

---

## Tool: rank_documents

Rank documents by importance and relevance.

### Request
```json
{
  "topic": "string"
}
```

**Parameters:**
- `topic` (optional, string): Filter by topic (omit for all)

### Response
```json
{
  "success": true,
  "data": {
    "ranked_documents": [
      {
        "filename": "algebra_comprehensive.txt",
        "filepath": "study_materials/algebra_comprehensive.txt",
        "importance_score": 0.95,
        "size": 50000,
        "reasons": [
          "Contains summary information",
          "Includes practical exercises",
          "Comprehensive document"
        ]
      },
      {
        "filename": "algebra_intro.txt",
        "filepath": "study_materials/algebra_intro.txt",
        "importance_score": 0.75,
        "size": 25000,
        "reasons": [
          "Includes practical exercises"
        ]
      }
    ],
    "total_documents": 2,
    "ranking_criteria": [
      "Contains summaries and overviews",
      "Includes practical exercises",
      "Has important references",
      "Document comprehensiveness",
      "Topic relevance"
    ],
    "timestamp": "2024-01-15T10:30:45.123456"
  }
}
```

**Response Fields:**
- `ranked_documents`: Sorted list of documents
- `total_documents`: Total number of ranked documents
- `ranking_criteria`: Factors affecting ranking
- `timestamp`: When ranking was performed

**Document Fields:**
- `filename`: Document file name
- `filepath`: Full path
- `importance_score`: Importance score (0.0-1.0)
- `size`: Document size
- `reasons`: Why this document is important

### Examples

**Example 1: All Documents**
```python
request = {}
```

**Example 2: Mathematics Only**
```python
request = {
  "topic": "Mathematics"
}
```

---

## Error Codes

| Code | HTTP | Description | Resolution |
|------|------|-------------|-----------|
| INVALID_QUERY | 400 | Empty search query | Provide non-empty query |
| INVALID_TOPIC | 400 | Empty topic name | Provide valid topic |
| INVALID_TOPICS | 400 | One/both topics empty | Provide both topics |
| EMPTY_MATERIALS | 404 | No study materials | Add files to study_materials/ |
| FILE_NOT_FOUND | 404 | Document not found | Check file exists |
| INVALID_FILE_FORMAT | 400 | Unsupported format | Use .txt, .pdf, or .md |
| DOCUMENT_PROCESSING_FAILED | 500 | Processing error | Check file encoding |
| INTERNAL_ERROR | 500 | Unexpected error | Check server logs |

---

## Best Practices

### Queries
- Use specific keywords
- Keep queries under 100 characters
- Use natural language
- Include context if helpful

### Topic Names
- Use exact spelling
- Capitalize properly
- Use compound names for specifics
- Avoid abbreviations when possible

### Handling Results
- Always check `success` field first
- Use `confidence` for result quality
- Review `snippets` for context
- Follow `source_files` to original documents

### Error Handling
```python
def safe_api_call(tool_name, **params):
    response = server.call_tool(tool_name, **params)
    
    if not response['success']:
        error = response['error']
        print(f"Error {error['code']}: {error['message']}")
        if error.get('hint'):
            print(f"Hint: {error['hint']}")
        return None
    
    return response['data']
```

---

## Rate Limiting

Current implementation has no rate limiting. For production:

```python
from functools import wraps
from time import time, sleep

def rate_limit(max_calls_per_second=10):
    min_interval = 1.0 / max_calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time() - last_called[0]
            if elapsed < min_interval:
                sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time()
            return result
        return wrapper
    return decorator
```

---

## Pagination

Current API doesn't support pagination. Use `top_k` parameter to limit results:

```python
# Get first 5 results
response1 = server.call_tool("search_material", query="...", top_k=5)

# Get first 20 results
response2 = server.call_tool("search_material", query="...", top_k=20)
```

---

## Caching Behavior

Caching is automatic:
- Embeddings cached for 24 hours
- Topics cached until materials change
- Document index cached in memory

Clear cache manually:
```python
# Clear cache files
import os
os.remove("cache/embeddings_cache.json")
os.remove("cache/topics.json")

# Restart server to rebuild
```

---

## Version History

- **v1.0.0** (2024-01-15): Initial release
  - 7 core tools
  - Document indexing
  - Keyword-based search
  - Topic extraction
  - Categorization and ranking
