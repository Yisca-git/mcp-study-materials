# Getting Started with Study Materials MCP Server

## Quick Start

### 1. Install Dependencies

```bash
cd study-materials-mcp
pip install -r requirements.txt
```

### 2. Add Sample Materials

Create sample files in the `study_materials/` directory:

**study_materials/algebra_basics.txt**
```
ALGEBRA BASICS

Introduction to Algebra:
Algebra is a branch of mathematics dealing with symbols and the rules for manipulating those symbols.
Key concepts include variables, expressions, equations, and functions.

Variables and Expressions:
A variable is a symbol (usually a letter) that represents an unknown number.
An algebraic expression is a combination of variables, numbers, and operations.

Solving Equations:
To solve an equation means to find the value of the variable that makes the equation true.
Common techxxxxxxxinclude combining like terms, using the distributive property, and inverse operations.

Exercises:
1. Simplify: 3x + 2x - 5 = ?
2. Solve for x: 2x + 10 = 20
3. Factor: x^2 + 5x + 6
```

### 3. Run the Server

```bash
python main.py
```

You should see:
```
Study Materials MCP Server
==================================================
Available tools: 7
  - search_material: Search study materials using semantic and keyword matching
  - explain_topic: Generate explanation of a topic from study materials
  - compare_topics: Compare two topics based on available materials
  - list_topics: List all recognized topics in study materials
  - find_knowledge_gaps: Analyze gaps in knowledge based on available materials
  - categorize_documents: Categorize documents by topic and subtopic
  - rank_documents: Rank documents by importance score

Server ready to process requests.
```

### 4. Test the Tools

Create a test script `test_server.py`:

```python
from main import StudyMaterialMCPServer

# Initialize server
server = StudyMaterialMCPServer()

# Test search
print("=== SEARCH TEST ===")
result = server.call_tool("search_material", query="What is algebra?", top_k=3)
print(f"Search results: {result['data']['results_count']} found")

# Test list topics
print("\n=== LIST TOPICS TEST ===")
result = server.call_tool("list_topics")
print(f"Topics: {result['data']['topics']}")

# Test explain topic
print("\n=== EXPLAIN TOPIC TEST ===")
result = server.call_tool("explain_topic", topic="Algebra")
if result['success']:
    print(f"Explanation:\n{result['data']['explanation'][:500]}...")

# Test categorize documents
print("\n=== CATEGORIZE DOCUMENTS TEST ===")
result = server.call_tool("categorize_documents")
if result['success']:
    print(f"Categories: {list(result['data']['categorization'].keys())}")

# Test rank documents
print("\n=== RANK DOCUMENTS TEST ===")
result = server.call_tool("rank_documents")
if result['success']:
    for doc in result['data']['ranked_documents'][:3]:
        print(f"  - {doc['filename']}: {doc['importance_score']:.2f}")
```

Run the test:
```bash
python test_server.py
```

## Architecture Overview

The server follows a modular design consistent with the git-mcp-server project:

```
���������������������������������������������
���  main.py    ���  MCP Server entry point
���������������������������������������������
       ���
       ������������ ������������������������������������������������������������������������
       ���    ���  StudyMaterialTools  ���  Tool implementations
       ���    ������������������������������������������������������������������������
       ���               ���
       ������������ ���������������������������������������������������������������������������������������������������������
            ���  StudyMaterialService           ���  Core business logic
            ���  - search_material              ���
            ���  - explain_topic                ���
            ���  - compare_topics               ���
            ���  - categorize_documents         ���
            ���  - rank_documents               ���
            ������������������������������������������������������������������������������������������������������������
                         ���
            ���������������������������������������������������������������������������������
            ���            ���            ���
       ������������������������������  ������������������������������������  ������������������������������������������������
       ��� Models ���  ��� Services ���  ��� Utils        ���
       ��� - Data ���  ��� - Process���  ��� - Validation ���
       ��� Classes���  ��� Documents���  ��� - Paths      ���
       ������������������������������  ������������������������������������  ��� - Text       ���
                                 ��� - Errors     ���
                                 ������������������������������������������������
```

## Adding More Study Materials

Simply add more files to `study_materials/`:

**study_materials/geometry_fundamentals.txt**
```
GEOMETRY FUNDAMENTALS

Basic Concepts:
Geometry is the study of shapes, sizes, and properties of figures.

Key Shapes:
- Triangles: Three-sided polygons
- Rectangles: Four-sided figures with right angles
- Circles: Round shapes with all points equidistant from center

Important Theorems:
- Pythagorean Theorem: a�� + b�� = c��
- Area of triangle: A = (1/2) �� base �� height
```

The server will automatically index and make these materials searchable.

## Monitoring and Debugging

Enable detailed logging by setting environment variables:

```bash
export LOG_LEVEL=DEBUG  # On Windows: set LOG_LEVEL=DEBUG
python main.py
```

## Next Steps

1. Add more study materials to the `study_materials/` directory
2. Experiment with different search queries
3. Compare related topics to deepen understanding
4. Use the categorization tool to organize materials
5. Leverage the importance ranking to prioritize learning
6. Check knowledge gaps to identify missing topics

## Performance Tips

- Start with 10-50 documents for best performance
- Keep individual documents under 1 MB for optimal processing
- Use clear, structured formatting in your materials
- Add summaries and key points at the beginning of documents
- Include practice exercises to boost importance scores

## Troubleshooting

### No results from search
- Check that materials exist in `study_materials/`
- Verify file formats are supported (.txt, .pdf, .md)
- Try broader search queries

### Topics not recognized
- Ensure documents have clear topic markers or headers
- Keywords are extracted from content, so clear writing helps
- File names also contribute to topic identification

### Slow performance
- Reduce document size or number
- Clear cache directory to force reprocessing
- Reduce `CHUNK_SIZE` in `settings.py` for faster processing
