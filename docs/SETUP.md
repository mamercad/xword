# Xword Development Setup

Complete guide to setting up Xword development environment with `uv` and `ruff`.

## Quick Start

### 1. Install uv (Ultra-fast Python package installer)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (using PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify installation:**
```bash
uv --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/mamercad/xword.git
cd xword
```

### 3. Create Virtual Environment with uv

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 4. Install Dependencies with uv

```bash
# Install all dependencies
uv pip install -e .

# Or install with development tools
uv pip install -e ".[dev]"
```

### 5. Verify Installation

```bash
# Check that main dependencies are installed
python3 -c "import xword; print('xword version', xword.__version__)"

# Check ruff is available
ruff --version

# Try running a basic command
xword show examples/simple.md
```

## Using uv

### Installation

uv is an ultra-fast Python package installer and resolver written in Rust.

```bash
# Install a package
uv pip install pytest

# Install from local package (editable mode)
uv pip install -e .

# Install with extras
uv pip install -e ".[dev,docs]"

# Create a virtual environment
uv venv

# Sync environment to lock file
uv pip sync requirements.txt
```

### Benefits of uv

- **10-100x faster** than pip
- **Zero overhead** Python package manager
- **Lock file support** with `uv pip compile`
- **Dependency resolution** in milliseconds
- **Works with all Python packages** (fully compatible with pip)

## Using Ruff

### What is Ruff?

Ruff is an extremely fast Python linter and code formatter, written in Rust. It combines the functionality of:
- **pylint** - Code quality
- **isort** - Import sorting  
- **black** - Code formatting (via ruff format)
- **flake8** - Common issues
- **bugbear** - Common bugs
- **And more...**

All in one tool that is 10-100x faster.

### Linting

Check code for issues:

```bash
# Check current directory
ruff check .

# Check specific file or directory
ruff check xword/core/

# Show detailed output
ruff check . --show-fixes

# Show statistics
ruff check . --statistics
```

### Auto-fix Issues

Fix automatically:

```bash
# Fix all issues that can be auto-fixed
ruff check . --fix

# Preview fixes before applying
ruff check . --fix --show-fixes

# Allow unsafe fixes (those that might change behavior)
ruff check . --fix --unsafe-fixes
```

### Formatting (with `ruff format`)

Format code consistently:

```bash
# Format current directory
ruff format .

# Format specific files
ruff format xword/core/models.py tests/

# Check without modifying
ruff format . --check
```

### Configuration

Ruff configuration is in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = [
    "E", "W",  # pycodestyle
    "F",       # pyflakes
    "I",       # isort
    "N",       # pep8-naming
    "UP",      # pyupgrade
    "B",       # flake8-bugbear
    "A",       # flake8-builtins
    "C4",      # flake8-comprehensions
    "RUF",     # ruff-specific
]

ignore = [
    "E501",    # line too long (handled by black)
    "E741",    # ambiguous variable name
]
```

## Development Workflow

### 1. Setup Once

```bash
# Clone and enter directory
git clone https://github.com/mamercad/xword.git
cd xword

# Create virtual environment
uv venv
source .venv/bin/activate

# Install development dependencies
uv pip install -e ".[dev]"
```

### 2. Regular Development

```bash
# Run tests
pytest tests/

# Check code quality with ruff
ruff check xword/ tests/

# Auto-fix issues
ruff check xword/ tests/ --fix

# Format code
ruff format xword/ tests/

# Run specific test
pytest tests/unit/test_puzzle_parser.py
```

### 3. Before Committing

```bash
# Comprehensive check
ruff check xword/ tests/ --statistics
ruff format xword/ tests/ --check
pytest tests/

# If all pass, commit!
git add .
git commit -m "message"
```

## Complete Workflow Example

```bash
# 1. Start fresh
cd xword
source .venv/bin/activate

# 2. Make your changes
# ... edit some files ...

# 3. Check code quality
ruff check xword/ tests/

# 4. Fix issues automatically
ruff check xword/ tests/ --fix

# 5. Format code
ruff format xword/ tests/

# 6. Run tests
pytest tests/

# 7. Check again
ruff check xword/ tests/ --statistics

# 8. Commit
git add .
git commit -m "feat(module): description of changes"

# 9. Push
git push origin main
```

## Useful Commands

### Development Tools

```bash
# Run pytest with coverage
pytest --cov=xword tests/

# Run specific test with verbose output
pytest tests/unit/test_puzzle_parser.py -v

# Run tests that match pattern
pytest -k "test_parse" -v

# Run with output capture disabled (see print statements)
pytest -s
```

### Code Quality

```bash
# Comprehensive lint report
ruff check . --show-fixes --statistics

# Check specific rule
ruff check . --select=E501

# Ignore specific rule
ruff check . --ignore=E501

# Show all violations even if not auto-fixable
ruff check . --extend-ignore=none
```

### Virtual Environment

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Deactivate
deactivate

# Remove and recreate
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Troubleshooting

### uv issues

**Problem:** `command not found: uv`

**Solution:** Make sure uv is in PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
uv --version
```

**Problem:** Virtual environment not activating

**Solution:** Check the path:
```bash
source .venv/bin/activate
echo $VIRTUAL_ENV  # Should show path to .venv
```

### ruff issues

**Problem:** `No module named ruff`

**Solution:** Install with uv:
```bash
uv pip install ruff
```

**Problem:** Ruff config file errors

**Solution:** Validate `pyproject.toml`:
```bash
ruff check . --show-fixes
```

### Tests failing

**Problem:** Import errors in tests

**Solution:** Install in development mode:
```bash
uv pip install -e .
```

**Problem:** Tests can't find modules

**Solution:** Make sure virtual environment is activated:
```bash
source .venv/bin/activate
which python  # Should show path to .venv
```

## Pre-commit Hook (Optional)

Setup automatic linting before commits:

```bash
# Install pre-commit
uv pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.0.292
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
EOF

# Install the git hook
pre-commit install

# Test it
pre-commit run --all-files
```

Now ruff will automatically run on commit!

## Continuous Integration

GitHub Actions workflow (`.github/workflows/lint.yml`):

```yaml
name: Lint and Format

on: [push, pull_request]

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: astral-sh/ruff-action@v1
        with:
          args: 'check . --show-fixes'
      - uses: astral-sh/ruff-action@v1
        with:
          command: format
          args: '--check'
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: |
          pip install -e ".[dev]"
          pytest tests/
```

## Performance Tips

### uv Performance

- Use uv with `--index-strategy=fastest-match` for faster resolution
- Cache downloads in `UV_CACHE_DIR`
- Use lock files for reproducible installs

### ruff Performance

- Run ruff in parallel with `--jobs` (done automatically)
- Only check changed files: `ruff check $(git diff --name-only)`
- Use `--extend-ignore` to skip slow checks temporarily

## Further Reading

- [uv Documentation](https://github.com/astral-sh/uv)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Xword Development Guide](DEVELOPMENT.md)
- [Contributing Guide](../CONTRIBUTING.md)
