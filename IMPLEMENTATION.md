# Study Materials MCP Server - Implementation Guide

## Project Overview

This is a complete MCP (Model Context Protocol) server implementation for managing, searching, and analyzing study materials. It follows the same architectural patterns as the git-mcp-server project.

## Architecture Design

### Core Components

#### 1. Models Layer (`models/`)
Defines all data structures using Python dataclasses:

- **result.py**: `ToolResult`, `ErrorInfo` - Standardized response formats
- **study_material_models.py**: `Document`, `DocumentChunk`, `SearchResult`, `TopicInfo` - Domain models

#### 2. Services Layer (`services/`)
Implements business logic and core functionality:

- **document_processor.py**: `DocumentProcessor`
  - Loads and processes various file formats (TXT, PDF, MD)
  - Creates document chunks for processing
  - Extracts keywords and metadata

- **study_material_service.py**: `StudyMaterialService`
  - Core service for all operations
  - Implements search, explain, compare, categorize, and rank functions
  - Manages document indexing and caching
  - Handles all error cases gracefully

#### 3. Utils Layer (`utils/`)
Provides utility functions and helpers:

- **errors.py**: Error codes for consistent error handling
- **paths.py**: Path manipulation and validation
- **validate.py**: Input validation functions
- **text_processing.py**: Text chunking, keyword extraction, snippet generation

#### 4. Tools Layer (`tools/`)
Implements MCP tool handlers:

- **study_material_tools.py**: `StudyMaterialTools`
  - Wraps service methods
  - Formats responses for MCP protocol
  - Handles tool invocation

### Data Flow

```
User Request
    ↓
main.py (StudyMaterialMCPServer)
    ↓
study_material_tools.py (StudyMaterialTools)
    ↓
study_material_service.py (StudyMaterialService)
    ├→ services/document_processor.py
    └→ utils/ (validation, text processing)
    ↓
models/ (ToolResult, ErrorInfo)
    ↓
Response
```

## Key Features

### 1. Search Material
- **Keyword matching**: Frequency-based search with stopword filtering
- **Text similarity**: Jaccard similarity on extracted keywords
- **Snippet extraction**: Context-aware snippet generation
- **Top-K results**: Returns top N most relevant documents

### 2. Explain Topic
- **Aggregated explanation**: Compiles information from multiple sources
- **Related topics**: Finds semantically related topics
- **Source tracking**: Lists which documents were used

### 3. Compare Topics
- **Similarity analysis**: Finds common themes between topics
- **Difference extraction**: Highlights differences
- **Source comparison**: Shows which materials cover each topic

### 4. List Topics
- **Automatic extraction**: Pulls topics from document content
- **Keyword-based**: Uses top keywords from each document
- **Filename-based**: Also considers document names

### 5. Find Knowledge Gaps
- **Confidence scoring**: Evaluates confidence level
- **Gap identification**: Identifies missing information
- **Recommendations**: Suggests what materials to add

### 6. Categorize Documents
- **Automatic inference**: Determines category from filename/content
- **Supported categories**: Math, Physics, Chemistry, Biology, CS, History, Literature
- **Extensible**: Easy to add new categories

### 7. Rank Documents
- **Multi-factor scoring**:
  - Summary indicators (+0.1 per summary keyword)
  - Exercise/practice content (+0.15 per exercise keyword)
  - References/citations (+0.1 per reference keyword)
  - File size (+0.2 max)
  - Topic relevance (+0.15 bonus)
- **Reasons tracking**: Explains why a document was ranked highly

## Configuration

Edit `settings.py` to customize:

```python
MATERIALS_DIR = "study_materials"  # Document storage location
CACHE_DIR = "cache"                # Cache storage location
SUPPORTED_FORMATS = ["txt", "pdf", "md"]
CHUNK_SIZE = 500                   # Characters per chunk
CHUNK_OVERLAP = 50                 # Overlap between chunks
MAX_SNIPPETS = 3                   # Results per snippet
DEFAULT_TOP_K = 5                  # Default search results
MAX_TOP_K = 20                     # Maximum searchable results
IMPORTANCE_THRESHOLD = 0.5         # Min importance score
```

## Extension Points

### Adding New Tools

1. Add method to `StudyMaterialService`
2. Add wrapper to `StudyMaterialTools`
3. Add tool definition in `main.py`
4. Update test files

### Adding New Categories

In `study_material_service.py`, update `_infer_category()`:

```python
def _infer_category(self, filename: str, content: str) -> str:
    categories_keywords = {
        "New Category": ["keyword1", "keyword2", "keyword3"],
        # ... existing categories ...
    }
```

### Custom Importance Metrics

Override `_calculate_importance()` in `StudyMaterialService`:

```python
def _calculate_importance(self, filename: str, content: str, topic: str = "") -> float:
    score = 0.5
    # Add custom scoring logic
    return min(1.0, score)
```

## Error Handling

All operations return structured error responses:

```python
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable message",
        "hint": "Optional hint for resolution",
        "details": {"contextual": "information"}
    }
}
```

Common error codes:
- `INVALID_QUERY`: Empty or invalid search query
- `INVALID_TOPIC`: Empty or invalid topic
- `EMPTY_MATERIALS`: No documents in materials directory
- `FILE_NOT_FOUND`: Document file not found
- `INVALID_FILE_FORMAT`: Unsupported file type

## Performance Optimization

### Caching Strategy
- Embeddings cached in `cache/embeddings_cache.json`
- Topics cached in `cache/topics.json`
- Document index stored in memory

### Lazy Loading
- Documents loaded only when needed
- Files not read until first query

### Efficient Search
- Keyword matching before text similarity
- Early exit if results found
- Limit snippet extraction to top results

## Testing

### Test Structure
```
tests/
├── test_search.py      # Search functionality
├── test_topic.py       # Topic operations
└── test_documents.py   # Document operations (future)
```

### Running Tests
```bash
pytest tests/
pytest tests/test_search.py -v
pytest tests/test_topic.py -v
```

### Adding Tests
```python
def test_feature(service):
    """Test description."""
    result = service.operation()
    assert result.ok
    assert "expected" in result.data
```

## File Format Support

### Plain Text (.txt)
- Direct file reading
- Fastest processing
- Full-text searchable

### Markdown (.md)
- Same as TXT (extension-based)
- Preserves formatting
- Good for structured content

### PDF (.pdf)
- Requires PyPDF2
- Text extraction from pages
- Falls back to placeholder if library unavailable

To add PDF support:
```bash
pip install PyPDF2
```

## Database and Caching

### Current Implementation
- In-memory document index
- JSON file caching for embeddings and topics
- No external database required

### Future Enhancement (FAISS)
For large-scale deployments:
```python
import faiss

# Create FAISS index
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)

# Fast similarity search
distances, indices = index.search(query_embedding, top_k)
```

## Integration with AI Agents

The server is designed to be called by AI agents through MCP protocol:

```python
# AI Agent Call Example
server = StudyMaterialMCPServer()

# Agent requests available tools
tools = server.get_tools()

# Agent calls a tool
response = server.call_tool(
    "search_material",
    query="What is machine learning?",
    top_k=5
)

# Agent processes response
if response['success']:
    results = response['data']['results']
    # Use results to inform agent decisions
```

## Troubleshooting

### No results from search
- Verify materials exist in `study_materials/`
- Check file formats are supported
- Try simpler search terms
- Check for encoding issues in files

### Slow performance
- Reduce number of documents
- Reduce document size
- Increase `CHUNK_SIZE` in settings
- Clear cache directory

### Memory issues
- Process documents in batches
- Implement external database
- Use FAISS for large embeddings

## Future Enhancements

- [ ] Vector embeddings with transformers
- [ ] FAISS vector database integration
- [ ] Named Entity Recognition (NER)
- [ ] Advanced PDF processing
- [ ] Document versioning
- [ ] User authentication
- [ ] REST API wrapper
- [ ] Web UI
- [ ] Multi-language support
- [ ] Custom embedding models

## Dependencies

```
python-dotenv==1.0.0   # Environment variables
PyPDF2==3.0.1          # PDF processing (optional)
```

Development dependencies:
```
pytest>=7.0.0          # Testing
pytest-asyncio>=0.21.0 # Async testing
black>=23.0.0          # Code formatting
pylint>=2.0.0          # Code linting
```

## Contributing

1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass
5. Use type hints throughout

## License

MIT License - See LICENSE file for details
