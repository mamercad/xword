"""Crossword puzzle engine."""

import time

from xword.core.models import Cell, Clue, Direction, Grid, PuzzleDefinition, PuzzleSession


class PuzzleEngine:
    """Engine for managing and validating crossword puzzles."""

    def __init__(self):
        """Initialize the puzzle engine."""
        self.sessions: dict[str, PuzzleSession] = {}

    def create_session(
        self, puzzle_id: str, puzzle: PuzzleDefinition, user_id: str
    ) -> PuzzleSession:
        """Create a new puzzle session."""
        # Create a copy of the grid for the session
        session_grid = Grid(puzzle.grid.rows, puzzle.grid.cols)
        for (row, col), cell in puzzle.grid.cells.items():
            new_cell = Cell(
                row=cell.row,
                col=cell.col,
                letter=cell.letter,
                is_black=cell.is_black,
                clue_numbers=cell.clue_numbers.copy(),
            )
            session_grid.set_cell(row, col, new_cell)

        session = PuzzleSession(
            puzzle_id=puzzle_id,
            puzzle=puzzle,
            grid=session_grid,
            start_time=time.time(),
            participants={user_id},
        )
        self.sessions[puzzle_id] = session
        return session

    def set_cell_entry(
        self, puzzle_id: str, row: int, col: int, letter: str | None
    ) -> bool:
        """Set a user entry in a cell. Returns True if valid."""
        if puzzle_id not in self.sessions:
            return False

        session = self.sessions[puzzle_id]
        cell = session.grid.get_cell(row, col)

        if cell is None or cell.is_black or cell.is_empty():
            return False

        # Allow empty entry or single letter
        if letter is not None and len(letter) > 1:
            return False

        cell.user_entry = letter.upper() if letter else None
        return True

    def get_clue_for_cell(
        self, puzzle_id: str, row: int, col: int, direction: Direction
    ) -> Clue | None:
        """Get the clue that applies to a cell in a given direction."""
        if puzzle_id not in self.sessions:
            return None

        session = self.sessions[puzzle_id]
        cell = session.grid.get_cell(row, col)

        if cell is None or cell.is_black:
            return None

        clue_number = cell.clue_numbers.get(direction)
        if clue_number is None:
            return None

        clues = session.puzzle.across_clues if direction == Direction.ACROSS else session.puzzle.down_clues
        for clue in clues:
            if clue.number == clue_number:
                return clue

        return None

    def get_cells_for_clue(
        self, puzzle_id: str, clue: Clue
    ) -> list[Cell]:
        """Get all cells for a clue."""
        if puzzle_id not in self.sessions:
            return []

        session = self.sessions[puzzle_id]
        cells = []
        for row, col in clue.cells:
            cell = session.grid.get_cell(row, col)
            if cell:
                cells.append(cell)
        return cells

    def check_clue(self, puzzle_id: str, clue: Clue) -> bool:
        """Check if a clue is completely and correctly filled."""
        cells = self.get_cells_for_clue(puzzle_id, clue)
        if not cells or len(cells) != clue.length:
            return False

        for cell in cells:
            if not cell.is_correct():
                return False

        return True

    def check_puzzle(self, puzzle_id: str) -> bool:
        """Check if the entire puzzle is solved."""
        if puzzle_id not in self.sessions:
            return False

        session = self.sessions[puzzle_id]
        for clue in session.puzzle.all_clues():
            if not self.check_clue(puzzle_id, clue):
                return False

        return True

    def complete_session(self, puzzle_id: str) -> bool:
        """Mark a session as completed."""
        if puzzle_id not in self.sessions:
            return False

        session = self.sessions[puzzle_id]
        if self.check_puzzle(puzzle_id):
            session.is_completed = True
            session.completed_at = time.time()
            return True

        return False

    def get_hint(self, puzzle_id: str, clue: Clue) -> str:
        """Get a hint for a clue (reveal one letter)."""
        cells = self.get_cells_for_clue(puzzle_id, clue)
        if not cells:
            return ""

        # Find the first unrevealed cell and reveal it
        for cell in cells:
            if cell.user_entry is None:
                cell.user_entry = cell.letter
                return cell.letter

        # All cells revealed
        return ""

    def get_session(self, puzzle_id: str) -> PuzzleSession | None:
        """Get a session by puzzle ID."""
        return self.sessions.get(puzzle_id)

    def add_participant(self, puzzle_id: str, user_id: str) -> bool:
        """Add a participant to a session."""
        if puzzle_id not in self.sessions:
            return False

        self.sessions[puzzle_id].participants.add(user_id)
        return True
