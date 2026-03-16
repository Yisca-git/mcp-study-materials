# Study Materials MCP Server

Advanced Model Context Protocol (MCP) server for organizing, searching, and interacting with study materials. This server provides AI coding agents with powerful tools to semantically search, categorize, and analyze educational documents.

## Features

- **Semantic Search**: Find relevant study materials using keyword and semantic matching
- **Topic Explanation**: Generate comprehensive explanations of topics from available materials
- **Topic Comparison**: Compare and contrast different topics based on content
- **Knowledge Gap Analysis**: Identify missing information and areas for improvement
- **Document Categorization**: Automatically organize materials by topic and subtopic
- **Importance Ranking**: Rank documents based on their significance and content type
- **Dynamic Indexing**: Automatically indexes new materials added to the directory

## Project Structure

```
study-materials-mcp/
├── models/
│   ├── result.py              # ToolResult and ErrorInfo classes
│   └── study_material_models.py  # Document and SearchResult models
├── services/
│   ├── document_processor.py   # Document loading and processing
│   └── study_material_service.py  # Core service logic
├── tools/
│   └── study_material_tools.py  # MCP tool implementations
├── utils/
│   ├── errors.py              # Error codes
│   ├── paths.py               # Path utilities
│   ├── text_processing.py     # Text processing functions
│   └── validate.py            # Validation functions
├── tests/
│   ├── test_search.py
│   └── test_topic.py
├── main.py                    # Server entry point
├── settings.py                # Configuration
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Add Study Materials

Place your PDF, TXT, or Markdown files in the `study_materials/` directory:

```
study_materials/
├── algebra_basics.txt
├── calculus_fundamentals.pdf
└── physics_mechanics.md
```

### Start the Server

```bash
python main.py
```

### Available Tools

#### 1. search_material
Search study materials using semantic and keyword matching.

```python
{
    "query": "What is algebra?",
    "top_k": 5
}
```

Response:
```json
{
    "success": true,
    "data": {
        "query": "What is algebra?",
        "results_count": 3,
        "results": [
            {
                "filename": "algebra_basics.txt",
                "relevance_score": 10.5,
                "snippets": ["...relevant text..."],
                "confidence": 0.95
            }
        ],
        "confidence": 0.95
    }
}
```

#### 2. explain_topic
Generate explanation of a specific topic.

```python
{
    "topic": "Algebra"
}
```

#### 3. compare_topics
Compare two topics based on available materials.

```python
{
    "topic1": "Algebra",
    "topic2": "Geometry"
}
```

#### 4. list_topics
Get list of all recognized topics.

```python
{}
```

#### 5. find_knowledge_gaps
Analyze gaps in knowledge for a given topic.

```python
{
    "query": "Advanced Calculus"
}
```

#### 6. categorize_documents
Organize documents by topic and subtopic.

```python
{}
```

#### 7. rank_documents
Rank documents by importance score.

```python
{
    "topic": "Mathematics"  # Optional
}
```

## Architecture

### Models

- **ToolResult**: Standardized response format with ok/error status
- **ErrorInfo**: Error information with code, message, and details
- **DocumentChunk**: Represents a chunk of a document with embeddings
- **Document**: Full document with metadata and chunks
- **SearchResult**: Search result with relevance scoring

### Services

- **DocumentProcessor**: Handles loading and processing various file formats
- **StudyMaterialService**: Core logic for search, categorization, and analysis

### Text Processing

- Keyword extraction using frequency analysis
- Text chunking with overlapping windows
- Snippet extraction around query matches
- Text similarity calculation
- Stopword filtering

## Configuration

Edit `settings.py` to customize:

```python
MATERIALS_DIR = "study_materials"  # Where to load materials
CACHE_DIR = "cache"                # Where to store cache
CHUNK_SIZE = 500                   # Text chunk size
CHUNK_OVERLAP = 50                 # Overlap between chunks
MAX_SNIPPETS = 3                   # Snippets per result
DEFAULT_TOP_K = 5                  # Default search results
```

## Error Handling

All operations return structured error responses:

```json
{
    "success": false,
    "error": {
        "code": "INVALID_QUERY",
        "message": "Query cannot be empty.",
        "hint": "Provide a non-empty search query",
        "details": {"query": ""}
    }
}
```

## Performance Optimization

- **Caching**: Embeddings and topics are cached to avoid recalculation
- **Lazy Loading**: Documents are loaded only when needed
- **Efficient Search**: Keyword matching combined with similarity scores

## Testing

Run tests using pytest:

```bash
pytest tests/
```

## Future Enhancements

- [ ] Vector embedding using transformers (all-MiniLM-L6-v2)
- [ ] FAISS integration for large-scale similarity search
- [ ] Named Entity Recognition (NER) for enhanced topic extraction
- [ ] PDF text extraction improvements
- [ ] Web UI for document management
- [ ] Batch document processing
- [ ] Export categorization to file system

## License

MIT License

## Contributing

Contributions are welcome! Please ensure:

- Code follows the existing style
- Tests are included for new features
- Documentation is updated
