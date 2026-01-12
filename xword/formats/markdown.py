"""Markdown-based crossword puzzle format."""

import re

from xword.core.models import Cell, Clue, Direction, Grid, PuzzleDefinition


class MarkdownParser:
    """Parser for Markdown-based crossword puzzles.
    
    Format:
    # Puzzle Title
    Description here
    
    ## Grid
    ```
      1 2 3
    1 C A T
    2 A . .
    3 T . .
    ```
    
    ## Across
    1. Domestic animal (3)
    2. First letter (1)
    
    ## Down
    1. Feline pet (3)
    2. First letter (1)
    """

    @staticmethod
    def parse(content: str) -> PuzzleDefinition:
        """Parse a markdown puzzle definition."""
        lines = content.split("\n")

        title = ""
        description = ""
        grid_lines = []
        across_clues = []
        down_clues = []

        current_section = None

        i = 0
        while i < len(lines):
            line = lines[i]

            # Parse title
            if line.startswith("# ") and not title:
                title = line[2:].strip()
                i += 1
                continue

            # Parse description (lines before first ## section)
            if line and not line.startswith("#") and current_section is None and title:
                if not grid_lines or not line.startswith("##"):
                    description += line + "\n"
                    i += 1
                    continue

            # Parse sections
            if line.startswith("## "):
                current_section = line[3:].strip().lower()
                i += 1
                continue

            # Parse grid
            if current_section == "grid":
                if line.startswith("```"):
                    i += 1
                    continue
                if line.strip() == "":
                    i += 1
                    continue
                grid_lines.append(line)

            # Parse clues
            elif current_section in ("across", "down"):
                match = re.match(r"^(\d+)\.\s+(.+?)\s*\((\d+)\)\s*$", line.strip())
                if match:
                    number = int(match.group(1))
                    text = match.group(2)
                    length = int(match.group(3))

                    clue = Clue(
                        number=number,
                        direction=Direction.ACROSS if current_section == "across" else Direction.DOWN,
                        text=text,
                        start_row=0,  # Will be filled after grid parsing
                        start_col=0,
                        length=length,
                    )

                    if current_section == "across":
                        across_clues.append(clue)
                    else:
                        down_clues.append(clue)

            i += 1

        # Parse grid
        grid, solution = MarkdownParser._parse_grid(grid_lines)

        # Map clues to grid positions and cells
        MarkdownParser._map_clues_to_grid(grid, across_clues, down_clues, solution)

        puzzle = PuzzleDefinition(
            title=title.strip(),
            description=description.strip(),
            grid=grid,
            across_clues=across_clues,
            down_clues=down_clues,
        )

        return puzzle

    @staticmethod
    def _parse_grid(grid_lines: list[str]) -> tuple[Grid, dict]:
        """Parse the grid from markdown format.
        
        Returns (Grid, solution_dict) where solution_dict maps (row, col) to letter.
        """
        if not grid_lines:
            raise ValueError("No grid found")

        # Find dimensions
        rows = len(grid_lines) - 1  # First line is header with column numbers

        # Parse first data line to get columns
        first_line = grid_lines[1] if len(grid_lines) > 1 else ""
        cells_in_first = [c.strip() for c in first_line.split() if c.strip()]
        cols = len(cells_in_first)

        grid = Grid(rows, cols)
        solution = {}

        # Parse grid cells
        for i, line in enumerate(grid_lines[1:]):  # Skip header
            parts = [p.strip() for p in line.split() if p.strip()]
            row_num = int(parts[0])
            row_idx = row_num - 1

            for j, cell_str in enumerate(parts[1:]):
                col_idx = j

                cell = Cell(row=row_idx, col=col_idx)

                if cell_str == ".":
                    cell.is_black = True
                else:
                    cell.letter = cell_str.upper()
                    solution[(row_idx, col_idx)] = cell_str.upper()

                grid.set_cell(row_idx, col_idx, cell)

        return grid, solution

    @staticmethod
    def _map_clues_to_grid(grid: Grid, across_clues: list[Clue], down_clues: list[Clue], solution: dict) -> None:
        """Map clues to their positions in the grid."""
        # Find clue starting positions
        clue_positions = {}  # (row, col) -> (across_number, down_number)

        across_by_num = {c.number: c for c in across_clues}
        down_by_num = {c.number: c for c in down_clues}

        for row in range(grid.rows):
            for col in range(grid.cols):
                cell = grid.get_cell(row, col)
                if cell and not cell.is_black:
                    # Check if this starts an across clue
                    if col == 0 or (grid.get_cell(row, col - 1) and grid.get_cell(row, col - 1).is_black):
                        # Find the length of this across
                        length = 0
                        c = col
                        while c < grid.cols and grid.get_cell(row, c) and not grid.get_cell(row, c).is_black:
                            length += 1
                            c += 1

                        if length > 1:
                            # Find clue with this number and direction
                            for clue in across_clues:
                                if clue.length == length and clue.start_row == 0:  # Not yet assigned
                                    clue.start_row = row
                                    clue.start_col = col
                                    cells = []
                                    for x in range(col, col + length):
                                        cells.append((row, x))
                                    clue.cells = cells
                                    if (row, col) in solution:
                                        clue.answer = "".join(solution[(row, x)] for x in range(col, col + length))
                                    break

                    # Check if this starts a down clue
                    if row == 0 or (grid.get_cell(row - 1, col) and grid.get_cell(row - 1, col).is_black):
                        # Find the length of this down
                        length = 0
                        r = row
                        while r < grid.rows and grid.get_cell(r, col) and not grid.get_cell(r, col).is_black:
                            length += 1
                            r += 1

                        if length > 1:
                            # Find clue with this number and direction
                            for clue in down_clues:
                                if clue.length == length and clue.start_row == 0:  # Not yet assigned
                                    clue.start_row = row
                                    clue.start_col = col
                                    cells = []
                                    for y in range(row, row + length):
                                        cells.append((y, col))
                                    clue.cells = cells
                                    if (row, col) in solution:
                                        clue.answer = "".join(solution[(y, col)] for y in range(row, row + length))
                                    break

        # Assign clue numbers to cells
        across_num = 1
        down_num = 1

        for row in range(grid.rows):
            for col in range(grid.cols):
                cell = grid.get_cell(row, col)
                if cell and not cell.is_black:
                    has_across = False
                    has_down = False

                    # Check if this is start of across
                    if col == 0 or (grid.get_cell(row, col - 1) and grid.get_cell(row, col - 1).is_black):
                        c = col
                        length = 0
                        while c < grid.cols and grid.get_cell(row, c) and not grid.get_cell(row, c).is_black:
                            length += 1
                            c += 1
                        if length > 1:
                            cell.clue_numbers[Direction.ACROSS] = across_num
                            has_across = True

                    # Check if this is start of down
                    if row == 0 or (grid.get_cell(row - 1, col) and grid.get_cell(row - 1, col).is_black):
                        r = row
                        length = 0
                        while r < grid.rows and grid.get_cell(r, col) and not grid.get_cell(r, col).is_black:
                            length += 1
                            r += 1
                        if length > 1:
                            cell.clue_numbers[Direction.DOWN] = down_num
                            has_down = True

                    if has_across:
                        across_num += 1
                    if has_down:
                        down_num += 1
