"""Data models for crossword puzzles."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class Direction(str, Enum):
    """Direction of a clue."""

    ACROSS = "across"
    DOWN = "down"


@dataclass
class Cell:
    """A single cell in the crossword grid."""

    row: int
    col: int
    letter: Optional[str] = None  # The solution letter
    is_black: bool = False  # Whether this is a black/blocked cell
    user_entry: Optional[str] = None  # What the user has entered
    clue_numbers: Dict[Direction, int] = field(default_factory=dict)

    def is_empty(self) -> bool:
        """Check if cell is empty (no letter)."""
        return self.letter is None or self.letter.strip() == ""

    def is_correct(self) -> bool:
        """Check if user entry matches the solution."""
        if self.is_black or self.is_empty():
            return True
        return self.user_entry and self.user_entry.upper() == self.letter.upper()

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "row": self.row,
            "col": self.col,
            "letter": self.letter,
            "is_black": self.is_black,
            "user_entry": self.user_entry,
            "clue_numbers": self.clue_numbers,
        }


@dataclass
class Clue:
    """A crossword clue."""

    number: int
    direction: Direction
    text: str
    start_row: int
    start_col: int
    length: int
    cells: List[Tuple[int, int]] = field(default_factory=list)  # (row, col) coordinates
    answer: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "number": self.number,
            "direction": self.direction.value,
            "text": self.text,
            "start_row": self.start_row,
            "start_col": self.start_col,
            "length": self.length,
            "cells": self.cells,
            "answer": self.answer,
        }


@dataclass
class Grid:
    """A crossword grid."""

    rows: int
    cols: int
    cells: Dict[Tuple[int, int], Cell] = field(default_factory=dict)

    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """Get a cell at the given position."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells.get((row, col))
        return None

    def set_cell(self, row: int, col: int, cell: Cell) -> None:
        """Set a cell at the given position."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[(row, col)] = cell

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "rows": self.rows,
            "cols": self.cols,
            "cells": {str(k): v.to_dict() for k, v in self.cells.items()},
        }


@dataclass
class PuzzleDefinition:
    """Definition of a crossword puzzle."""

    title: str
    description: str
    grid: Grid
    across_clues: List[Clue] = field(default_factory=list)
    down_clues: List[Clue] = field(default_factory=list)
    difficulty: str = "medium"  # easy, medium, hard
    source: Optional[str] = None  # Where the puzzle came from

    def all_clues(self) -> List[Clue]:
        """Get all clues."""
        return self.across_clues + self.down_clues

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "title": self.title,
            "description": self.description,
            "grid": self.grid.to_dict(),
            "across_clues": [c.to_dict() for c in self.across_clues],
            "down_clues": [c.to_dict() for c in self.down_clues],
            "difficulty": self.difficulty,
            "source": self.source,
        }


@dataclass
class PuzzleSession:
    """An active puzzle solving session."""

    puzzle_id: str
    puzzle: PuzzleDefinition
    grid: Grid  # Copy of the grid with user entries
    start_time: float
    participants: Set[str] = field(default_factory=set)
    is_completed: bool = False
    completed_at: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "puzzle_id": self.puzzle_id,
            "puzzle": self.puzzle.to_dict(),
            "grid": self.grid.to_dict(),
            "start_time": self.start_time,
            "participants": list(self.participants),
            "is_completed": self.is_completed,
            "completed_at": self.completed_at,
        }
