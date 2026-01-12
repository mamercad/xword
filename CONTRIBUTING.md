# Contributing to Xword

Thank you for your interest in contributing to xword! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and follow our code of conduct.

- Be respectful and inclusive
- Assume good faith
- Focus on constructive feedback
- Welcome diverse perspectives

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Follow the setup instructions in DEVELOPMENT.md

## How to Contribute

### Reporting Bugs

- Check if the bug has been reported
- Include version info, platform, and reproduction steps
- Provide minimal reproducible example
- Attach error logs or screenshots

### Suggesting Features

- Check if feature has been requested
- Explain the use case
- Describe expected behavior
- Suggest implementation approach (optional)

### Contributing Code

1. **Fork and branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes**
   - Follow code style (Black, Ruff)
   - Add tests for new functionality
   - Update documentation

3. **Test**
   ```bash
   pytest tests/
   black xword/ tests/
   ruff check xword/ tests/
   ```

4. **Commit**
   ```bash
   git commit -m "feat(scope): description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   ```

### Adding Example Puzzles

Puzzles are great ways to showcase the format and test functionality!

1. Create a `.md` file in `examples/`
2. Follow the format in PUZZLE_FORMAT.md
3. Include a meaningful title and description
4. Test with: `python -m xword.cli show examples/your-puzzle.md`
5. Submit in PR or issue

### Writing Tests

Tests should be:
- **Clear**: Describe what's being tested
- **Isolated**: Independent of other tests
- **Fast**: Complete in milliseconds
- **Deterministic**: Same result every time

Example:
```python
def test_feature_name():
    """Clear description of what this tests."""
    # Arrange
    input_data = "test input"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == "expected output"
```

### Documentation

- Keep docs up to date with code changes
- Use clear, concise language
- Include examples and diagrams
- Link to related sections

## Commit Message Format

Use conventional commits for consistency:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Test additions/changes
- `ci`: CI/CD changes
- `chore`: Build, dependencies, etc.

Examples:
```
feat(puzzle): add automatic clue numbering
fix(parser): handle grid with odd spacing
docs(format): clarify black cell syntax
test(engine): add validation tests
refactor(core): simplify cell comparison
```

## Pull Request Process

1. **Update README** if needed
2. **Add tests** for new functionality
3. **Update docs** for API changes
4. **Ensure all tests pass**
5. **Keep PR focused** on single feature/fix
6. **Respond to review feedback** promptly
7. **Squash commits** if requested

### PR Title Format
```
[Type] Brief description
```

Examples:
- `[Feature] Add Wikipedia clue generation`
- `[Fix] Correct grid parsing edge case`
- `[Docs] Improve puzzle format guide`

## Review Guidelines

We appreciate reviews! When reviewing PRs:

- Check code quality and style
- Verify tests are adequate
- Ensure documentation is clear
- Test functionality if possible
- Be constructive and kind
- Suggest alternatives, not just criticism

## Project Setup

See DEVELOPMENT.md for detailed setup instructions.

Quick start:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/
```

## Branching Strategy

- `main`: Stable, released code
- Feature branches: `feature/name`
- Bug fixes: `fix/name`
- Chores: `chore/name`

## Release Process

Releases are managed by maintainers. When released:
1. Version bumped in `pyproject.toml`
2. CHANGELOG updated
3. Git tag created
4. Package published to PyPI

## Getting Help

- **Discussions**: Use GitHub discussions for questions
- **Issues**: Report bugs and request features
- **Documentation**: Check docs first
- **Community**: Join community chat (planned)

## Areas Looking for Help

### High Priority
- [ ] Console TUI implementation with Textual
- [ ] Server multiplayer features
- [ ] Comprehensive test suite
- [ ] Documentation and examples

### Medium Priority
- [ ] Additional puzzle format parsers
- [ ] Wikipedia integration
- [ ] Performance optimizations
- [ ] CI/CD pipeline setup

### Good for Beginners
- [ ] Documentation improvements
- [ ] Example puzzle creation
- [ ] Comment improvements
- [ ] Bug fixes and edge cases

## Code Style

### Python

Follow PEP 8 with Black defaults (100 char lines):

```python
# Good
def calculate_puzzle_completion(puzzle: PuzzleDefinition) -> float:
    """Calculate completion percentage."""
    total = len(puzzle.across_clues) + len(puzzle.down_clues)
    return (completed / total) * 100

# Avoid
def calc_puzz_completion(p):
    return (completed / (len(p.across_clues) + len(p.down_clues))) * 100
```

### Naming Conventions

- Classes: `PascalCase` (PuzzleEngine)
- Functions/methods: `snake_case` (set_cell_entry)
- Constants: `UPPER_SNAKE_CASE` (MAX_GRID_SIZE)
- Private: `_leading_underscore` (_internal_method)

### Type Hints

Encouraged but not required:
```python
from typing import Optional, List

def get_clues(
    puzzle: PuzzleDefinition,
    direction: Direction
) -> List[Clue]:
    """Get clues in a specific direction."""
    ...
```

### Docstrings

Use Google style:
```python
def calculate_score(
    correct: int,
    total: int,
    time_seconds: int
) -> float:
    """Calculate puzzle solving score.
    
    Args:
        correct: Number of correct cells
        total: Total number of cells
        time_seconds: Time taken in seconds
    
    Returns:
        Score from 0.0 to 100.0
    
    Raises:
        ValueError: If time_seconds is negative
    """
```

## Performance Considerations

When contributing, consider:
- Avoid O(n²) algorithms where possible
- Cache frequently accessed data
- Use generators for large iterations
- Profile performance-critical code
- Add performance notes in comments

## Accessibility

- Use semantic HTML in web UI
- Include alt text for images
- Ensure keyboard navigation works
- Test with screen readers
- Use sufficient color contrast

## Security

- Never commit secrets or credentials
- Validate all user input
- Sanitize external data
- Report security issues privately
- Follow OWASP guidelines

## Legal

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open an issue for discussion
- Comment on related issues
- Reach out to maintainers
- Check existing documentation

Thank you for contributing to xword! 🎉
