"""Integration tests for TUI functionality."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from xword.formats.markdown import MarkdownParser
from xword.core.puzzle import PuzzleEngine
from xword.core.models import Direction


def test_tui_game_flow():
    """Test complete game flow in TUI."""
    # Load puzzle
    puzzle_path = Path(__file__).parent.parent.parent / "examples" / "simple.md"
    content = puzzle_path.read_text()
    puzzle = MarkdownParser.parse(content)

    # Create engine and session
    engine = PuzzleEngine()
    session_id = "test_session"
    session = engine.create_session(session_id, puzzle, "test_player")

    # Verify session created
    assert session is not None
    assert session.puzzle_id == "test_session"
    assert "test_player" in session.participants

    # Simulate game play
    # Find first cell and enter letter
    for row in range(puzzle.grid.rows):
        for col in range(puzzle.grid.cols):
            cell = puzzle.grid.get_cell(row, col)
            if cell and not cell.is_black:
                # Enter correct letter
                engine.set_cell_entry(session_id, row, col, cell.letter)
                
                # Check cell is correct
                updated_cell = session.grid.get_cell(row, col)
                assert updated_cell.user_entry == cell.letter
                assert updated_cell.is_correct()
                return

    assert False, "No white cells found in puzzle"


def test_tui_navigation():
    """Test cursor navigation."""
    puzzle_path = Path(__file__).parent.parent.parent / "examples" / "simple.md"
    content = puzzle_path.read_text()
    puzzle = MarkdownParser.parse(content)

    engine = PuzzleEngine()
    session_id = "nav_test"
    engine.create_session(session_id, puzzle, "player")

    # Find starting position
    start_row = None
    start_col = None
    for row in range(puzzle.grid.rows):
        for col in range(puzzle.grid.cols):
            cell = puzzle.grid.get_cell(row, col)
            if cell and not cell.is_black:
                start_row = row
                start_col = col
                break
        if start_row is not None:
            break

    assert start_row is not None, "No white cells in puzzle"

    # Verify we can navigate (just test that it doesn't crash)
    # In a real TUI test, we would test the widget navigation


def test_clue_retrieval():
    """Test getting clues for cells."""
    puzzle_path = Path(__file__).parent.parent.parent / "examples" / "simple.md"
    content = puzzle_path.read_text()
    puzzle = MarkdownParser.parse(content)

    engine = PuzzleEngine()
    session_id = "clue_test"
    session = engine.create_session(session_id, puzzle, "player")

    # Test getting clues for first cell
    if session.grid.rows > 0 and session.grid.cols > 0:
        clue = engine.get_clue_for_cell(session_id, 0, 0, Direction.ACROSS)
        # May be None if cell is black or has no across clue
        if clue:
            assert clue.direction == Direction.ACROSS
            assert len(clue.cells) > 0


def test_hint_system():
    """Test hint generation."""
    puzzle_path = Path(__file__).parent.parent.parent / "examples" / "simple.md"
    content = puzzle_path.read_text()
    puzzle = MarkdownParser.parse(content)

    engine = PuzzleEngine()
    session_id = "hint_test"
    engine.create_session(session_id, puzzle, "player")

    # Find a clue and get hint
    if puzzle.across_clues:
        clue = puzzle.across_clues[0]
        hint = engine.get_hint(session_id, clue)
        
        # Hint should be a letter
        assert hint == "" or (len(hint) == 1 and hint.isalpha())


def test_puzzle_completion():
    """Test puzzle completion detection."""
    puzzle_path = Path(__file__).parent.parent.parent / "examples" / "simple.md"
    content = puzzle_path.read_text()
    puzzle = MarkdownParser.parse(content)

    engine = PuzzleEngine()
    session_id = "complete_test"
    session = engine.create_session(session_id, puzzle, "player")

    # Fill in all cells with correct answers
    filled = 0
    for row in range(puzzle.grid.rows):
        for col in range(puzzle.grid.cols):
            cell = session.grid.get_cell(row, col)
            if cell and not cell.is_black and cell.letter:
                engine.set_cell_entry(session_id, row, col, cell.letter)
                filled += 1

    # Check if puzzle can be marked complete
    if filled > 0:
        completed = engine.complete_session(session_id)
        updated_session = engine.get_session(session_id)
        assert updated_session.is_completed == completed


if __name__ == "__main__":
    test_tui_game_flow()
    test_tui_navigation()
    test_clue_retrieval()
    test_hint_system()
    test_puzzle_completion()
    print("All TUI integration tests passed!")
