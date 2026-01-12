"""Custom Textual widgets for xword TUI."""

from textual.reactive import reactive
from textual.widgets import Static


class HelpPanel(Static):
    """Display keyboard shortcuts and help."""

    def __init__(self):
        super().__init__()
        self.border_title = "Help"

    def render(self) -> str:
        """Render help information."""
        return """[bold]Keyboard Shortcuts[/bold]

[cyan]Navigation[/cyan]
  ↑↓←→  Move cursor
  Tab   Switch direction

[cyan]Editing[/cyan]
  A-Z   Enter letter
  Backspace / Delete  Clear cell
  Ctrl+U  Undo entry
  Ctrl+R  Redo entry

[cyan]Game[/cyan]
  Ctrl+H  Hint (reveal one letter)
  Ctrl+C  Check puzzle
  Ctrl+S  Save progress
  Q       Quit game

[cyan]Colors[/cyan]
  [green]Green[/green]  - Correct answer
  White  - Incorrect
  [black]Black[/black]  - Blocked cell
"""


class StatsPanel(Static):
    """Display game statistics."""

    total_cells = reactive(0)
    filled_cells = reactive(0)
    correct_cells = reactive(0)
    time_elapsed = reactive(0)

    def __init__(self):
        super().__init__()
        self.border_title = "Stats"

    def render(self) -> str:
        """Render statistics."""
        percent = 0
        if self.total_cells > 0:
            percent = (self.correct_cells / self.total_cells) * 100

        return f"""[bold]Puzzle Progress[/bold]

Filled:  {self.filled_cells}/{self.total_cells}
Correct: {self.correct_cells}/{self.total_cells}
Progress: {percent:.0f}%

Time: {self.time_elapsed // 60}m {self.time_elapsed % 60}s
"""


class InputPrompt(Static):
    """Simple input prompt for letter entry."""

    def __init__(self):
        super().__init__()
        self.border_title = "Entry"

    def render(self) -> str:
        """Render input prompt."""
        return "[dim]Type letters to fill cells[/dim]\n[dim]Use arrow keys to navigate[/dim]"
