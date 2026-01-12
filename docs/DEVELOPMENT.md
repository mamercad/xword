# Development Guide

## Getting Started

### Prerequisites

- Python 3.10 or later
- pip or conda

### Setup

1. Clone the repository:
```bash
git clone https://github.com/mamercad/xword.git
cd xword
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest tests/
```

## Project Structure

```
xword/
├── xword/                    # Main package
│   ├── __init__.py
│   ├── cli.py               # CLI entry point
│   ├── core/                # Core game logic
│   │   ├── __init__.py
│   │   ├── models.py        # Data models
│   │   └── puzzle.py        # Game engine
│   ├── formats/             # Puzzle format parsers
│   │   ├── __init__.py
│   │   └── markdown.py      # Markdown parser
│   ├── server/              # Server backend
│   │   ├── __init__.py
│   │   └── app.py           # FastAPI app
│   ├── tui/                 # Terminal UI
│   │   ├── __init__.py
│   │   └── app.py           # Textual app
│   ├── client/              # Client library
│   │   └── __init__.py
│   └── utils/               # Utilities
│       ├── __init__.py
│       └── wikipedia.py     # Wikipedia integration
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test fixtures
├── examples/               # Example puzzles
├── docs/                   # Documentation
├── pyproject.toml          # Project config
├── README.md              # Main readme
└── .gitignore
```

## Development Workflow

### Making Changes

1. Create a feature branch:
```bash
git checkout -b feature/my-feature
```

2. Make your changes following the code style guidelines

3. Run tests:
```bash
pytest tests/
```

4. Check code style:
```bash
black xword/ tests/
ruff check xword/ tests/
```

5. Commit with conventional messages:
```bash
git commit -m "feat(module): description"
```

### Code Style

- **Formatting**: Use `black` with line length 100
- **Linting**: Use `ruff` for imports and general issues
- **Type hints**: Encouraged but not required for MVP
- **Docstrings**: Use Google-style docstrings

### Testing

Tests are organized by type:

**Unit Tests** (`tests/unit/`)
- Test individual functions/classes in isolation
- Use mocks for dependencies
- Should be fast

**Integration Tests** (`tests/integration/`)
- Test modules working together
- Use real file I/O and network calls
- Slower but more realistic

**Fixtures** (`tests/fixtures/`)
- Reusable test data
- Example puzzles for testing

Example test:
```python
import pytest
from xword.formats.markdown import MarkdownParser

def test_parse_simple_puzzle():
    content = """
    # Test Puzzle
    
    ## Grid
    ```
      1 2 3
    1 A B C
    2 D . E
    3 F G H
    ```
    
    ## Across
    1. First (3)
    
    ## Down
    1. Down (3)
    """
    
    puzzle = MarkdownParser.parse(content)
    assert puzzle.title == "Test Puzzle"
    assert puzzle.grid.rows == 3
    assert len(puzzle.across_clues) == 1
```

## Building Features

### Adding a New Puzzle Format

1. Create a new parser in `xword/formats/`:
```python
# xword/formats/across_lite.py

class AcrossLiteParser:
    @staticmethod
    def parse(content: str) -> PuzzleDefinition:
        # Implement parsing logic
        pass
```

2. Register in `xword/formats/__init__.py`:
```python
from xword.formats.across_lite import AcrossLiteParser

__all__ = ["MarkdownParser", "AcrossLiteParser"]
```

3. Add tests in `tests/formats/`:
```python
# tests/formats/test_across_lite.py

def test_parse_across_lite_puzzle():
    # Write test
    pass
```

### Adding a Server Endpoint

1. Add route to `xword/server/app.py`:
```python
@app.get("/puzzles/{puzzle_id}")
async def get_puzzle(puzzle_id: str):
    puzzle = puzzle_engine.get_puzzle(puzzle_id)
    if not puzzle:
        raise HTTPException(status_code=404)
    return puzzle.to_dict()
```

2. Add integration test:
```python
# tests/integration/test_server.py

@pytest.mark.asyncio
async def test_get_puzzle_endpoint(client):
    response = await client.get("/puzzles/simple")
    assert response.status_code == 200
```

### Adding TUI Features

1. Create new widget in `xword/tui/`:
```python
# xword/tui/widgets.py

from textual.widgets import Static

class GridWidget(Static):
    def __init__(self, puzzle):
        super().__init__()
        self.puzzle = puzzle
    
    def render(self):
        # Render grid
        pass
```

2. Add to main app in `xword/tui/app.py`:
```python
class XwordApp(Screen):
    def compose(self):
        yield Header()
        yield GridWidget(self.puzzle)
        yield CluePanel(self.puzzle)
        yield Footer()
```

## Common Tasks

### Running the CLI

```bash
# Show puzzle info
python -m xword.cli show examples/simple.md

# Play (once TUI is implemented)
python -m xword.cli play examples/simple.md

# Start server
python -m xword.cli serve -p 8000
```

### Testing Puzzle Parsing

```python
import sys
sys.path.insert(0, '.')

from xword.formats.markdown import MarkdownParser

with open('examples/simple.md', 'r') as f:
    puzzle = MarkdownParser.parse(f.read())

print(puzzle.title)
print(f"Grid: {puzzle.grid.rows}x{puzzle.grid.cols}")
```

### Creating Test Puzzles

Add to `examples/`:
```markdown
# My Test Puzzle

## Grid
...

## Across
...

## Down
...
```

## Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Using PDB

```python
import pdb; pdb.set_trace()
```

### Inspect Parsed Puzzle

```python
from xword.formats.markdown import MarkdownParser

puzzle = MarkdownParser.parse(content)
print(puzzle.grid.cells)
for clue in puzzle.across_clues:
    print(f"{clue.number}. {clue.text}: {clue.cells}")
```

## Documentation

### Building Docs

```bash
pip install -e ".[docs]"
mkdocs serve  # Local preview
mkdocs build  # Generate static site
```

### Writing Docs

- Use Markdown in `docs/`
- Reference code with `path:line` format
- Include examples and diagrams
- Update README.md for major changes

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG
3. Create git tag
4. Push to remote
5. Build distribution:
```bash
python -m build
twine upload dist/*
```

## Performance Considerations

### Puzzle Parsing

- Parsing is currently O(n) where n is content length
- Grid lookup is O(1) with dictionary representation
- Could cache parsed puzzles for repeated access

### Multiplayer Updates

- Currently broadcasts to all participants
- Consider room-based filtering for large servers
- Rate limit to prevent spam

## Architecture Decision Records

### Why Sparse Grid Representation?

- Crossword grids are typically sparse
- Dictionary lookup is O(1)
- Memory efficient for large grids
- Easy to extend with metadata

### Why Markdown Format?

- Human-readable and editable
- Version control friendly
- No external dependencies
- Easy to learn

### Why Textual?

- Pure Python, no C dependencies
- Cross-platform (works on any terminal)
- Rich feature set
- Active community

## Future Improvements

- [ ] Async puzzle loading
- [ ] Cached puzzle parsing
- [ ] Database persistence
- [ ] User authentication
- [ ] Puzzle rating/difficulty metrics
- [ ] Hint generation system
- [ ] Undo/redo support
- [ ] Mobile app support
