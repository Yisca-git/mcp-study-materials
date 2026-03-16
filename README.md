# study-materials-mcp

A Model Context Protocol (MCP) server that enables AI agents to search, analyze, and interact with study materials using semantic search, topic explanation, and knowledge gap analysis.

## Project Structure

```
study-materials-mcp/
├── models/
│   ├── result.py                  # ToolResult and ErrorInfo classes
│   └── study_material_models.py   # Document and SearchResult models
├── services/
│   ├── document_processor.py      # Document loading and processing
│   └── study_material_service.py  # Core service logic
├── tools/
│   └── study_material_tools.py    # MCP tool implementations
├── utils/
│   ├── errors.py                  # Error codes
│   ├── paths.py                   # Path utilities
│   ├── text_processing.py         # Text processing functions
│   └── validate.py                # Validation functions
├── tests/
│   ├── test_search.py
│   └── test_topic.py
├── study_materials/               # Place your study files here
├── main.py                        # Server entry point
├── settings.py                    # Configuration
└── requirements.txt
```

## Installation

1. Clone the repository and create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the example env file:
```bash
cp .env.example .env
```

## Usage

### 1. Add Study Materials

Place your `.txt`, `.pdf`, or `.md` files in the `study_materials/` directory:

```
study_materials/
├── algebra_basics.txt
├── calculus_fundamentals.pdf
└── physics_mechanics.md
```

### 2. Start the Server

```bash
python main.py
```

### 3. Connect an AI Agent

Configure your MCP-compatible client to connect to the server. See `mcp.example.json` for the tool schema.

## Tools

| Tool | Description |
|------|-------------|
| `search_material` | Search materials by keyword/semantic query |
| `explain_topic` | Generate an explanation of a topic from available materials |
| `compare_topics` | Compare and contrast two topics |
| `list_topics` | List all recognized topics |
| `find_knowledge_gaps` | Identify missing information for a topic |
| `categorize_documents` | Organize documents by topic and subtopic |
| `rank_documents` | Rank documents by importance score |

## Configuration

Edit `settings.py` or set environment variables:

| Setting | Default | Description |
|---------|---------|-------------|
| `MATERIALS_DIR` | `study_materials` | Directory to load materials from |
| `CACHE_DIR` | `cache` | Directory for cached data |
| `CHUNK_SIZE` | `500` | Text chunk size (characters) |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `DEFAULT_TOP_K` | `5` | Default number of search results |
| `MAX_TOP_K` | `20` | Maximum number of search results |

## Error Handling

All tools return a structured response:

```json
{
    "success": false,
    "error": {
        "code": "INVALID_QUERY",
        "message": "Query cannot be empty.",
        "hint": "Provide a non-empty search query"
    }
}
```

## Testing

```bash
pytest tests/
```

## Requirements

- Python 3.9+
- `mcp >= 1.0.0`
- `pydantic >= 2.0.0`
- `PyPDF2 == 3.0.1`
- `python-dotenv == 1.0.0`

## License

MIT
