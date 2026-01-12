"""Textual-based TUI application for xword."""

from textual.app import ComposeResult, Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Static, Label
from textual import on
from textual.binding import Binding

from xword.core.models import PuzzleDefinition


class GridDisplay(Static):
    """Display the crossword grid."""

    def __init__(self, puzzle: PuzzleDefinition):
        super().__init__()
        self.puzzle = puzzle

    def render(self) -> str:
        """Render the grid."""
        lines = []
        
        # Header with column numbers
        col_header = "   "
        for col in range(self.puzzle.grid.cols):
            col_header += f"{col+1:2} "
        lines.append(col_header)
        
        # Grid rows
        for row in range(self.puzzle.grid.rows):
            line = f"{row+1:2} "
            for col in range(self.puzzle.grid.cols):
                cell = self.puzzle.grid.get_cell(row, col)
                if cell and cell.is_black:
                    line += "## "
                elif cell:
                    entry = cell.user_entry or " "
                    clue_num = ""
                    for direction, num in cell.clue_numbers.items():
                        clue_num = str(num)
                        break
                    line += f"{entry:2}{clue_num:1}"
                else:
                    line += "   "
            lines.append(line)
        
        return "\n".join(lines)


class CluePanel(Static):
    """Display clues."""

    def __init__(self, puzzle: PuzzleDefinition):
        super().__init__()
        self.puzzle = puzzle

    def render(self) -> str:
        """Render the clues."""
        lines = ["ACROSS:", ""]
        
        for clue in self.puzzle.across_clues:
            lines.append(f"{clue.number}. {clue.text} ({clue.length})")
        
        lines.append("")
        lines.append("DOWN:")
        lines.append("")
        
        for clue in self.puzzle.down_clues:
            lines.append(f"{clue.number}. {clue.text} ({clue.length})")
        
        return "\n".join(lines)


class XwordApp:
    """Main TUI application."""

    def __init__(self, puzzle: PuzzleDefinition):
        """Initialize the app with a puzzle."""
        self.puzzle = puzzle

    def run(self):
        """Run the TUI."""
        print("TUI not yet implemented - puzzle loaded successfully!")
        print(f"Title: {self.puzzle.title}")
        print(f"Grid: {self.puzzle.grid.rows}x{self.puzzle.grid.cols}")
        print(f"Across: {len(self.puzzle.across_clues)}, Down: {len(self.puzzle.down_clues)}")
