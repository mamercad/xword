"""Crossword puzzle grid generator."""

from typing import Optional
from xword.core.models import Cell, Clue, Direction, Grid, PuzzleDefinition


class GridGenerator:
    """Generate a crossword grid from clues and answers."""

    def __init__(self):
        """Initialize the grid generator."""
        self.grid: Optional[Grid] = None
        self.placements: dict[tuple[int, int], tuple[str, Direction]] = {}

    def generate_from_clues(
        self,
        title: str,
        description: str,
        across_clues: list[tuple[int, str, int]],  # (number, text, length)
        down_clues: list[tuple[int, str, int]],
        answers: dict[int, str],  # clue_number -> answer
    ) -> PuzzleDefinition:
        """Generate a crossword puzzle from clues and answers.

        Args:
            title: Puzzle title
            description: Puzzle description
            across_clues: List of (number, text, length) tuples
            down_clues: List of (number, text, length) tuples
            answers: Dict mapping clue number to answer string

        Returns:
            PuzzleDefinition with generated grid
        """
        # Create clue objects
        across_objs = [
            Clue(
                number=num,
                direction=Direction.ACROSS,
                text=text,
                start_row=0,
                start_col=0,
                length=length,
                answer=answers.get(num, ""),
            )
            for num, text, length in across_clues
        ]
        down_objs = [
            Clue(
                number=num,
                direction=Direction.DOWN,
                text=text,
                start_row=0,
                start_col=0,
                length=length,
                answer=answers.get(num, ""),
            )
            for num, text, length in down_clues
        ]

        # Place words and create grid
        grid = self._create_grid(across_objs, down_objs)

        return PuzzleDefinition(
            title=title,
            description=description,
            grid=grid,
            across_clues=across_objs,
            down_clues=down_objs,
        )

    def _create_grid(self, across_clues: list[Clue], down_clues: list[Clue]) -> Grid:
        """Create grid by placing clues."""
        # Start with a large enough grid (we'll trim later)
        max_size = 50
        grid = Grid(max_size, max_size)

        # Initialize all cells
        for row in range(max_size):
            for col in range(max_size):
                grid.set_cell(row, col, Cell(row=row, col=col, is_black=True))

        # Place first across clue at (0, 0)
        if across_clues:
            self._place_across(grid, across_clues[0], 0, 0)

            # Place other across clues
            for clue in across_clues[1:]:
                placed = False
                # Try to place under/after existing clues
                for other in across_clues[: across_clues.index(clue)]:
                    if other.cells:
                        # Try placing below
                        row = other.start_row + 2
                        if row < max_size - clue.length:
                            if self._can_place_across(grid, clue, row, 0):
                                self._place_across(grid, clue, row, 0)
                                placed = True
                                break

                if not placed:
                    # Find a free row
                    for row in range(max_size):
                        if self._can_place_across(grid, clue, row, 0):
                            self._place_across(grid, clue, row, 0)
                            break

        # Place down clues
        for clue in down_clues:
            # Try to find intersections with across clues
            answer = clue.answer.upper() if clue.answer else ""

            for across_clue in across_clues:
                across_answer = across_clue.answer.upper() if across_clue.answer else ""

                # Find common letters
                for i, down_char in enumerate(answer):
                    for j, across_char in enumerate(across_answer):
                        if down_char == across_char:
                            # Try to place at intersection
                            row = across_clue.start_row - i
                            col = across_clue.start_col + j

                            if row >= 0 and col >= 0:
                                if self._can_place_down(grid, clue, row, col):
                                    self._place_down(grid, clue, row, col)
                                    break
                    else:
                        continue
                    break

        # Trim grid to used area
        grid = self._trim_grid(grid)

        # Assign clue numbers
        self._assign_clue_numbers(grid)

        return grid

    def _place_across(self, grid: Grid, clue: Clue, row: int, col: int) -> None:
        """Place an across clue in the grid."""
        answer = clue.answer.upper() if clue.answer else ""
        clue.start_row = row
        clue.start_col = col
        clue.cells = []

        for i, letter in enumerate(answer):
            cell = grid.get_cell(row, col + i)
            if cell is None:
                cell = Cell(row=row, col=col + i)

            cell.letter = letter
            cell.is_black = False
            grid.set_cell(row, col + i, cell)
            clue.cells.append((row, col + i))

    def _place_down(self, grid: Grid, clue: Clue, row: int, col: int) -> None:
        """Place a down clue in the grid."""
        answer = clue.answer.upper() if clue.answer else ""
        clue.start_row = row
        clue.start_col = col
        clue.cells = []

        for i, letter in enumerate(answer):
            cell = grid.get_cell(row + i, col)
            if cell is None:
                cell = Cell(row=row + i, col=col)

            cell.letter = letter
            cell.is_black = False
            grid.set_cell(row + i, col, cell)
            clue.cells.append((row + i, col))

    def _can_place_across(self, grid: Grid, clue: Clue, row: int, col: int) -> bool:
        """Check if an across clue can be placed."""
        answer = clue.answer.upper() if clue.answer else ""

        for i, letter in enumerate(answer):
            cell = grid.get_cell(row, col + i)
            if cell is None or (cell.letter and cell.letter != letter):
                return False

        return True

    def _can_place_down(self, grid: Grid, clue: Clue, row: int, col: int) -> bool:
        """Check if a down clue can be placed."""
        answer = clue.answer.upper() if clue.answer else ""

        for i, letter in enumerate(answer):
            cell = grid.get_cell(row + i, col)
            if cell is None or (cell.letter and cell.letter != letter):
                return False

        return True

    def _trim_grid(self, grid: Grid) -> Grid:
        """Trim grid to remove unused rows and columns."""
        # Find bounds of non-black cells
        min_row, max_row = float("inf"), -1
        min_col, max_col = float("inf"), -1

        for (row, col), cell in grid.cells.items():
            if not cell.is_black:
                min_row = min(min_row, row)
                max_row = max(max_row, row)
                min_col = min(min_col, col)
                max_col = max(max_col, col)

        if min_row == float("inf"):
            # Empty grid
            return Grid(1, 1)

        # Create new trimmed grid
        new_rows = max_row - min_row + 1
        new_cols = max_col - min_col + 1
        new_grid = Grid(new_rows, new_cols)

        for (row, col), cell in grid.cells.items():
            if min_row <= row <= max_row and min_col <= col <= max_col:
                new_row = row - min_row
                new_col = col - min_col
                new_cell = Cell(
                    row=new_row, col=new_col, letter=cell.letter, is_black=cell.is_black
                )
                new_grid.set_cell(new_row, new_col, new_cell)

        return new_grid

    def _assign_clue_numbers(self, grid: Grid) -> None:
        """Assign clue numbers to cells."""
        clue_num = 1

        for row in range(grid.rows):
            for col in range(grid.cols):
                cell = grid.get_cell(row, col)
                if cell and not cell.is_black:
                    # Check if this starts an across
                    starts_across = col == 0 or (
                        grid.get_cell(row, col - 1) and grid.get_cell(row, col - 1).is_black
                    )

                    # Check if this starts a down
                    starts_down = row == 0 or (
                        grid.get_cell(row - 1, col) and grid.get_cell(row - 1, col).is_black
                    )

                    # Check lengths
                    across_len = 1
                    c = col + 1
                    while (
                        c < grid.cols
                        and grid.get_cell(row, c)
                        and not grid.get_cell(row, c).is_black
                    ):
                        across_len += 1
                        c += 1

                    down_len = 1
                    r = row + 1
                    while (
                        r < grid.rows
                        and grid.get_cell(r, col)
                        and not grid.get_cell(r, col).is_black
                    ):
                        down_len += 1
                        r += 1

                    if (starts_across and across_len > 1) or (starts_down and down_len > 1):
                        if starts_across and across_len > 1:
                            cell.clue_numbers[Direction.ACROSS] = clue_num
                        if starts_down and down_len > 1:
                            cell.clue_numbers[Direction.DOWN] = clue_num
                        clue_num += 1
