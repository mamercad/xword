"""Display utilities for crossword puzzles."""

from xword.core.models import Grid, PuzzleDefinition, Direction


class GridDisplay:
    """Display crossword grids and puzzles."""

    @staticmethod
    def display_grid(grid: Grid, show_numbers: bool = True) -> str:
        """Display a grid as ASCII art.

        Args:
            grid: The grid to display
            show_numbers: Whether to show clue numbers

        Returns:
            ASCII representation of the grid
        """
        lines = []

        # Add each row
        for row in range(grid.rows):
            row_str = ""

            for col in range(grid.cols):
                cell = grid.get_cell(row, col)

                if cell is None:
                    row_str += " ? "
                elif cell.is_black:
                    row_str += " ██ "
                elif cell.letter:
                    row_str += f" {cell.letter} "
                else:
                    row_str += " . "

            lines.append(row_str)

        return "\n".join(lines)

    @staticmethod
    def display_puzzle(puzzle: PuzzleDefinition) -> str:
        """Display the complete puzzle with grid and clues.

        Args:
            puzzle: The puzzle to display

        Returns:
            Formatted puzzle display
        """
        output = []

        # Title
        output.append(f"# {puzzle.title}")
        output.append("")

        # Description
        if puzzle.description:
            output.append(puzzle.description)
            output.append("")

        # Grid
        output.append("## Grid")
        output.append("")
        output.append("```")
        output.append(GridDisplay.display_grid(puzzle.grid))
        output.append("```")
        output.append("")

        # Across clues
        if puzzle.across_clues:
            output.append("## Across")
            output.append("")
            for clue in puzzle.across_clues:
                output.append(f"{clue.number}. {clue.text} ({clue.length})")
            output.append("")

        # Down clues
        if puzzle.down_clues:
            output.append("## Down")
            output.append("")
            for clue in puzzle.down_clues:
                output.append(f"{clue.number}. {clue.text} ({clue.length})")
            output.append("")

        return "\n".join(output)

    @staticmethod
    def display_grid_with_clues(puzzle: PuzzleDefinition) -> str:
        """Display grid with clue numbers visible.

        Args:
            puzzle: The puzzle to display

        Returns:
            Grid display with clue numbers in cells
        """
        lines = []

        # Add each row
        for row in range(puzzle.grid.rows):
            row_str = ""

            for col in range(puzzle.grid.cols):
                cell = puzzle.grid.get_cell(row, col)

                if cell is None:
                    row_str += " ? "
                elif cell.is_black:
                    row_str += " ██ "
                else:
                    # Show clue number if it starts a clue, otherwise show letter
                    if cell.clue_numbers:
                        # Get the lowest numbered clue
                        num = min(cell.clue_numbers.values())
                        if num < 10:
                            row_str += f" {num} "
                        else:
                            row_str += f" {num}"
                    elif cell.letter:
                        row_str += f" {cell.letter} "
                    else:
                        row_str += " . "

            lines.append(row_str)

        return "\n".join(lines)
