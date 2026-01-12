"""Textual-based TUI application for xword."""

from textual.app import ComposeResult, on
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Header, Footer, Static, Input
from textual.binding import Binding
from textual.reactive import reactive

from xword.core.models import PuzzleDefinition, Direction, Cell
from xword.core.puzzle import PuzzleEngine


class GridDisplay(Static):
    """Display the crossword grid."""

    cursor_row = reactive(0)
    cursor_col = reactive(0)
    selected_direction = reactive(Direction.ACROSS)

    def __init__(self, puzzle: PuzzleDefinition, engine: PuzzleEngine, session_id: str):
        super().__init__()
        self.puzzle = puzzle
        self.engine = engine
        self.session_id = session_id
        self.border_title = "Grid"

    def render(self) -> str:
        """Render the grid."""
        lines = []
        
        session = self.engine.get_session(self.session_id)
        if not session:
            return "No active session"
        
        grid = session.grid
        
        # Header with column numbers
        col_header = "    "
        for col in range(grid.cols):
            col_header += f"{col+1:2} "
        lines.append(col_header)
        
        # Grid rows
        for row in range(grid.rows):
            line = f"{row+1:2} "
            for col in range(grid.cols):
                cell = grid.get_cell(row, col)
                
                # Highlight cursor position
                is_cursor = (row == self.cursor_row and col == self.cursor_col)
                
                if cell and cell.is_black:
                    if is_cursor:
                        line += "[reverse]##[/reverse] "
                    else:
                        line += "## "
                elif cell:
                    entry = cell.user_entry or "."
                    clue_num = ""
                    for direction in [Direction.ACROSS, Direction.DOWN]:
                        if direction in cell.clue_numbers:
                            clue_num = str(cell.clue_numbers[direction])
                            break
                    
                    # Color correct answers
                    if cell.is_correct() and cell.user_entry:
                        style = "[green]"
                        end_style = "[/green]"
                    else:
                        style = ""
                        end_style = ""
                    
                    cell_str = f"{style}{entry}{end_style}{clue_num:1}"
                    
                    if is_cursor:
                        line += f"[reverse]{cell_str}[/reverse]"
                    else:
                        line += cell_str
                    line += " "
                else:
                    if is_cursor:
                        line += "[reverse]?? [/reverse]"
                    else:
                        line += "?? "
            
            lines.append(line)
        
        return "\n".join(lines)

    def on_mount(self) -> None:
        """Initialize grid position."""
        # Find first non-black cell
        for row in range(self.puzzle.grid.rows):
            for col in range(self.puzzle.grid.cols):
                cell = self.puzzle.grid.get_cell(row, col)
                if cell and not cell.is_black:
                    self.cursor_row = row
                    self.cursor_col = col
                    return

    def get_current_cell(self) -> Cell | None:
        """Get the cell at cursor position."""
        session = self.engine.get_session(self.session_id)
        if not session:
            return None
        return session.grid.get_cell(self.cursor_row, self.cursor_col)

    def move_cursor(self, dr: int, dc: int) -> None:
        """Move cursor, skipping black cells."""
        session = self.engine.get_session(self.session_id)
        if not session:
            return

        new_row = self.cursor_row + dr
        new_col = self.cursor_col + dc

        # Wrap around grid edges
        if new_row < 0:
            new_row = session.grid.rows - 1
        elif new_row >= session.grid.rows:
            new_row = 0

        if new_col < 0:
            new_col = session.grid.cols - 1
        elif new_col >= session.grid.cols:
            new_col = 0

        # Skip black cells
        cell = session.grid.get_cell(new_row, new_col)
        if cell and not cell.is_black:
            self.cursor_row = new_row
            self.cursor_col = new_col


class CluePanel(Static):
    """Display clues with selection."""

    current_across = reactive(1)
    current_down = reactive(1)

    def __init__(self, puzzle: PuzzleDefinition):
        super().__init__()
        self.puzzle = puzzle
        self.border_title = "Clues"

    def render(self) -> str:
        """Render the clues."""
        lines = []
        
        lines.append("[bold]ACROSS[/bold]")
        lines.append("")
        
        for clue in self.puzzle.across_clues:
            if clue.number == self.current_across:
                lines.append(f"[reverse][bold]{clue.number}. {clue.text} ({clue.length})[/bold][/reverse]")
            else:
                lines.append(f"{clue.number}. {clue.text} ({clue.length})")
        
        lines.append("")
        lines.append("[bold]DOWN[/bold]")
        lines.append("")
        
        for clue in self.puzzle.down_clues:
            if clue.number == self.current_down:
                lines.append(f"[reverse][bold]{clue.number}. {clue.text} ({clue.length})[/bold][/reverse]")
            else:
                lines.append(f"{clue.number}. {clue.text} ({clue.length})")
        
        return "\n".join(lines)


class StatusBar(Static):
    """Status and help information."""

    def __init__(self, puzzle: PuzzleDefinition):
        super().__init__()
        self.puzzle = puzzle
        self.solved = 0
        self.total = len(puzzle.across_clues) + len(puzzle.down_clues)

    def render(self) -> str:
        """Render status bar."""
        return (
            f"[bold]{self.puzzle.title}[/bold] | "
            f"Solved: {self.solved}/{self.total} | "
            f"↑↓←→ Navigate | A-Z Type | Ctrl+H Hint | Q Quit"
        )


class XwordApp:
    """Main TUI application using Textual."""

    def __init__(self, puzzle: PuzzleDefinition):
        """Initialize the app with a puzzle."""
        self.puzzle = puzzle
        self.engine = PuzzleEngine()
        # Create a session
        self.session_id = "local_session"
        self.engine.create_session(self.session_id, puzzle, "player1")

    def run(self):
        """Run the TUI application."""
        from textual.app import App

        class XwordScreen(App):
            BINDINGS = [
                Binding("q", "quit", "Quit", show=True),
                ("up", "move_up", "Up"),
                ("down", "move_down", "Down"),
                ("left", "move_left", "Left"),
                ("right", "move_right", "Right"),
                ("ctrl+h", "hint", "Hint"),
                ("ctrl+c", "check", "Check"),
                ("backspace", "delete", "Delete"),
            ]

            def compose(self) -> ComposeResult:
                """Create child widgets for the app."""
                yield Header()
                
                with Horizontal():
                    with Vertical():
                        self.grid_display = GridDisplay(self.puzzle, self.engine, self.session_id)
                        yield self.grid_display
                        
                        self.status_bar = StatusBar(self.puzzle)
                        yield self.status_bar
                    
                    self.clue_panel = CluePanel(self.puzzle)
                    yield self.clue_panel
                
                yield Footer()

            def action_move_up(self) -> None:
                """Move cursor up."""
                self.grid_display.move_cursor(-1, 0)

            def action_move_down(self) -> None:
                """Move cursor down."""
                self.grid_display.move_cursor(1, 0)

            def action_move_left(self) -> None:
                """Move cursor left."""
                self.grid_display.move_cursor(0, -1)

            def action_move_right(self) -> None:
                """Move cursor right."""
                self.grid_display.move_cursor(0, 1)

            @on("input")
            def on_input(self, event) -> None:
                """Handle keyboard input for letter entry."""
                if event.character and event.character.isalpha():
                    cell = self.grid_display.get_current_cell()
                    if cell and not cell.is_black:
                        self.engine.set_cell_entry(
                            self.session_id,
                            self.grid_display.cursor_row,
                            self.grid_display.cursor_col,
                            event.character.upper(),
                        )
                        # Auto-advance to next cell
                        self.grid_display.move_cursor(0, 1)
                        self.refresh_grid()

            def action_delete(self) -> None:
                """Clear current cell."""
                cell = self.grid_display.get_current_cell()
                if cell and not cell.is_black:
                    self.engine.set_cell_entry(
                        self.session_id,
                        self.grid_display.cursor_row,
                        self.grid_display.cursor_col,
                        None,
                    )
                    self.refresh_grid()

            def action_hint(self) -> None:
                """Get a hint for the current cell."""
                cell = self.grid_display.get_current_cell()
                if not cell or cell.is_black:
                    return

                # Find clue for this cell
                clue = self.grid_display.puzzle.across_clues[0] if self.grid_display.puzzle.across_clues else None
                if clue:
                    self.engine.get_hint(self.session_id, clue)
                    self.refresh_grid()

            def action_check(self) -> None:
                """Check if puzzle is solved."""
                if self.engine.check_puzzle(self.session_id):
                    self.notify("🎉 Puzzle solved!")
                else:
                    self.notify("Not yet complete...")

            def refresh_grid(self) -> None:
                """Refresh the grid display."""
                self.grid_display.refresh()
                self.status_bar.refresh()

        app = XwordScreen()
        app.puzzle = self.puzzle
        app.engine = self.engine
        app.session_id = self.session_id
        app.run()
