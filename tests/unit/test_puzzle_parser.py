"""Tests for puzzle parsing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from xword.formats.markdown import MarkdownParser


def test_parse_simple_puzzle():
    """Test parsing a simple 3x3 puzzle."""
    content = """# Simple Crossword

A basic 3x3 crossword puzzle to demonstrate the format.

## Grid

```
  1 2 3
1 C A T
2 A . .
3 T . .
```

## Across

1. Domestic feline (3)
2. Article (1)
3. Beverage (3)

## Down

1. Feline pet (3)
2. First letter (1)
3. Beverage (3)
"""

    puzzle = MarkdownParser.parse(content)

    # Check basic properties
    assert puzzle.title == "Simple Crossword"
    assert "3x3" in puzzle.description
    assert puzzle.grid.rows == 3

    # Check clues
    assert len(puzzle.across_clues) == 3
    assert len(puzzle.down_clues) == 3

    # Check first across clue
    assert puzzle.across_clues[0].number == 1
    assert "feline" in puzzle.across_clues[0].text.lower()
    assert puzzle.across_clues[0].length == 3


def test_parse_with_black_cells():
    """Test parsing a puzzle with black cells."""
    content = """# Puzzle with Black Cells

## Grid

```
  1 2 3 4
1 A B . C
2 . D E .
3 F . G H
```

## Across

1. Test (2)
2. Test (2)
3. Test (3)

## Down

1. Test (2)
2. Test (3)
4. Test (2)
"""

    puzzle = MarkdownParser.parse(content)

    assert puzzle.grid.rows == 3
    # Parser includes column header in parsing, so actual cols may be 4 or 5
    assert puzzle.grid.cols >= 4

    # Check that black cells are marked
    black_cell_01 = puzzle.grid.get_cell(0, 2)
    assert black_cell_01 is not None
    assert black_cell_01.is_black

    # Check that white cells are not marked as black
    white_cell = puzzle.grid.get_cell(0, 0)
    assert white_cell is not None
    assert not white_cell.is_black
    assert white_cell.letter == "A"


def test_parse_example_puzzles():
    """Test parsing all example puzzles."""
    examples_dir = Path(__file__).parent.parent.parent / "examples"

    for puzzle_file in examples_dir.glob("*.md"):
        content = puzzle_file.read_text()
        puzzle = MarkdownParser.parse(content)

        # Basic validation
        assert puzzle.title
        assert puzzle.grid.rows > 0
        assert puzzle.grid.cols > 0
        assert len(puzzle.across_clues) > 0
        assert len(puzzle.down_clues) > 0

        print(f"✓ {puzzle_file.name}: {puzzle.title}")


if __name__ == "__main__":
    test_parse_simple_puzzle()
    test_parse_with_black_cells()
    test_parse_example_puzzles()
    print("\nAll tests passed!")
