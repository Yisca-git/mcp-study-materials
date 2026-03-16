# Study Materials MCP Server - Deployment Guide

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (optional, for version control)

### Installation Steps

1. **Clone or download the project**
```bash
cd study-materials-mcp
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Verify installation**
```bash
python main.py
```

You should see:
```
Study Materials MCP Server
==================================================
Available tools: 7
...
Server ready to process requests.
```

---

## Local Testing

### Running Sample Usage
```bash
python sample_usage.py
```

### Running Unit Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_search.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Manual Testing
Create `test_manual.py`:
```python
from main import StudyMaterialMCPServer

server = StudyMaterialMCPServer()

# Test search
result = server.call_tool("search_material", query="test", top_k=5)
print(result)

# Test list topics
result = server.call_tool("list_topics")
print(result)
```

Run with:
```bash
python test_manual.py
```

---

## Production Deployment

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p study_materials cache

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "main.py"]
```

Build and run:
```bash
# Build image
docker build -t study-materials-mcp:latest .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/study_materials:/app/study_materials \
  -v $(pwd)/cache:/app/cache \
  study-materials-mcp:latest
```

### Docker Compose Setup

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  study-materials-mcp:
    build: .
    container_name: study-materials-mcp
    ports:
      - "8000:8000"
    volumes:
      - ./study_materials:/app/study_materials
      - ./cache:/app/cache
    environment:
      - LOG_LEVEL=INFO
      - MATERIALS_DIR=/app/study_materials
      - CACHE_DIR=/app/cache
    restart: unless-stopped
```

Deploy:
```bash
docker-compose up -d
```

### Systemd Service (Linux)

Create `/etc/systemd/system/study-materials-mcp.service`:
```ini
[Unit]
Description=Study Materials MCP Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/study-materials-mcp
Environment="PATH=/opt/study-materials-mcp/venv/bin"
ExecStart=/opt/study-materials-mcp/venv/bin/python /opt/study-materials-mcp/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl start study-materials-mcp
sudo systemctl enable study-materials-mcp

# Check status
sudo systemctl status study-materials-mcp
```

### Windows Service

Using NSSM (Non-Sucking Service Manager):
```bash
# Install NSSM
choco install nssm

# Create service
nssm install StudyMaterialsMCP "C:\path\to\venv\Scripts\python.exe" "main.py"

# Set startup directory
nssm set StudyMaterialsMCP AppDirectory "C:\path\to\study-materials-mcp"

# Start service
nssm start StudyMaterialsMCP
```

---

## Environment Configuration

### Environment Variables

Create `.env` file:
```
# Server settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
LOG_LEVEL=INFO

# Paths
MATERIALS_DIR=./study_materials
CACHE_DIR=./cache

# Processing
CHUNK_SIZE=500
CHUNK_OVERLAP=50
MAX_SNIPPETS=3
DEFAULT_TOP_K=5
MAX_TOP_K=20
```

Load in Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()

materials_dir = os.getenv('MATERIALS_DIR', 'study_materials')
cache_dir = os.getenv('CACHE_DIR', 'cache')
log_level = os.getenv('LOG_LEVEL', 'INFO')
```

---

## Performance Tuning

### Optimization Strategies

#### 1. Chunk Size
Smaller chunks = more accurate search, slower processing
```python
settings.py:
CHUNK_SIZE = 300  # Smaller for accuracy
CHUNK_SIZE = 1000 # Larger for speed
```

#### 2. Caching
Clear cache to force reprocessing:
```bash
rm -rf cache/*
```

#### 3. Memory Usage
For large document sets:
```python
# Process in batches
batch_size = 100
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    process_batch(batch)
```

#### 4. Index Optimization
Pre-build indexes for faster queries:
```python
# In service initialization
def _build_indices(self):
    # Build keyword indices
    # Build topic indices
    # Cache aggressively
    pass
```

### Benchmarking

Create `benchmark.py`:
```python
import time
from main import StudyMaterialMCPServer

server = StudyMaterialMCPServer()

# Benchmark search
start = time.time()
for i in range(100):
    server.call_tool("search_material", query="test")
elapsed = time.time() - start
print(f"100 searches: {elapsed:.2f}s ({elapsed/100*1000:.2f}ms per query)")

# Benchmark other operations
start = time.time()
for i in range(10):
    server.call_tool("categorize_documents")
elapsed = time.time() - start
print(f"10 categorizations: {elapsed:.2f}s ({elapsed/10*1000:.2f}ms per op)")
```

---

## Monitoring and Logging

### Logging Configuration

Add to `main.py`:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Health Checks

Add endpoint:
```python
def health_check(self) -> dict:
    """Check server health."""
    return {
        "status": "healthy",
        "materials_count": len(self.documents),
        "topics_count": len(self.topics),
        "cache_size": os.path.getsize(self.cache_dir)
    }
```

### Metrics Collection

```python
from time import time
from collections import defaultdict

class MetricsCollector:
    def __init__(self):
        self.metrics = defaultdict(list)
    
    def record(self, operation, duration):
        self.metrics[operation].append(duration)
    
    def get_stats(self, operation):
        values = self.metrics[operation]
        return {
            "count": len(values),
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values)
        }
```

---

## Backup and Recovery

### Data Backup

Backup strategy:
```bash
# Daily backup
tar -czf backups/study_materials_$(date +%Y%m%d).tar.gz study_materials/ cache/

# Weekly backup
crontab -e
# Add: 0 0 * * 0 /path/to/backup.sh
```

### Cache Recovery

If cache becomes corrupted:
```bash
# Clear cache
rm -rf cache/*

# Restart server to rebuild
systemctl restart study-materials-mcp
```

### Document Recovery

Restore from backup:
```bash
# Stop server
systemctl stop study-materials-mcp

# Restore documents
tar -xzf backups/study_materials_20240115.tar.gz

# Start server
systemctl start study-materials-mcp
```

---

## Security Considerations

### Input Validation

Already implemented in utils/validate.py:
- Query validation
- Topic validation
- File path validation
- File format validation

### File Security

```python
# Prevent directory traversal
def safe_path_join(base, path):
    full = os.path.normpath(os.path.join(base, path))
    if not full.startswith(os.path.normpath(base)):
        raise ValueError("Path traversal attempt")
    return full
```

### Access Control

```python
# Add authentication if needed
from functools import wraps

def require_auth(func):
    @wraps(func)
    def wrapper(*args, auth_token=None, **kwargs):
        if not auth_token:
            raise ValueError("Authentication required")
        # Validate token
        return func(*args, **kwargs)
    return wrapper
```

---

## Scaling Strategies

### Horizontal Scaling

With load balancer (nginx):
```nginx
upstream study_materials {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

server {
    listen 80;
    location / {
        proxy_pass http://study_materials;
    }
}
```

### Vertical Scaling

Increase resources:
- More CPU cores
- Larger memory allocation
- SSD storage for cache

### Database Integration

For multi-instance setup, use shared database:
```python
# Add database layer for shared state
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@db:5432/study_materials')
# Use SQLAlchemy ORM for persistence
```

---

## Troubleshooting

### Common Issues

**Issue: No materials found**
- Check `study_materials/` directory exists
- Verify files are readable
- Check file extensions are .txt, .pdf, or .md

**Issue: Slow search performance**
- Reduce chunk size
- Limit document size
- Clear cache and rebuild

**Issue: High memory usage**
- Reduce document count
- Implement streaming
- Add database backend

**Issue: PDF extraction fails**
- Install PyPDF2: `pip install PyPDF2`
- Check PDF is valid
- Try converting to text format

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or via environment
export LOG_LEVEL=DEBUG
```

---

## Upgrade and Maintenance

### Version Updates

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests to verify
pytest tests/

# Restart service
systemctl restart study-materials-mcp
```

### Regular Maintenance

Weekly:
- Check disk space
- Review error logs
- Backup data

Monthly:
- Update dependencies
- Analyze performance metrics
- Clean old cache files

Quarterly:
- Major version updates
- Security patches
- Feature reviews

---

## Support and Debugging

### Getting Help

1. Check [API_REFERENCE.md](API_REFERENCE.md)
2. Review [IMPLEMENTATION.md](IMPLEMENTATION.md)
3. Check logs: `tail -f server.log`
4. Run tests: `pytest tests/ -v`

### Reporting Issues

Include:
- Error message
- Log output
- Environment details
- Steps to reproduce

---

## Advanced Features (Future)

- [ ] Vector database integration
- [ ] Distributed caching
- [ ] Real-time indexing
- [ ] Advanced NLP
- [ ] Web UI dashboard
- [ ] REST API
- [ ] GraphQL interface
- [ ] Multi-tenant support
