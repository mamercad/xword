# Xword Puzzle Format

## Markdown Format (Primary)

Xword uses a simple, human-readable Markdown-based format for defining crossword puzzles.

### Basic Structure

```markdown
# Puzzle Title

Optional description about the puzzle.

## Grid

```
  1 2 3 4 5
1 A B C D E
2 F . G . H
3 I J . K L
4 M . N O P
5 Q R S T U
```

## Across

1. Definition for across 1 (5)
3. Definition for across 3 (3)
5. Definition for across 5 (5)

## Down

1. Definition for down 1 (5)
2. Definition for down 2 (3)
3. Definition for down 3 (4)

```

### Components Explained

#### Title
Single line starting with `#` - must be the first heading
```markdown
# My Crossword Puzzle
```

#### Description
Any text between the title and the Grid section
```markdown
This is an optional description.
It can span multiple lines.
```

#### Grid Section

Starts with `## Grid` followed by a markdown code block.

Format:
- First row: column numbers, separated by spaces
- Subsequent rows: row number, followed by cell contents

Cell contents:
- **Letter**: Single uppercase letter (A-Z) for white cells with that letter
- **Dot (.)**: Black cell (blocked/no letter)
- **Spaces**: Used for alignment, multiple spaces indicate column separation

Example:
```
  1 2 3
1 C A T
2 A . .
3 T . .
```

This creates:
```
CAT
A..
T..
```

The grid is automatically analyzed to:
1. Identify black cells
2. Assign clue numbers to cell intersections
3. Group cells into answers
4. Validate clue lengths match actual grid dimensions

#### Clue Sections

**Across Clues** (`## Across`)
- Format: `NUMBER. CLUE TEXT (LENGTH)`
- Numbers must be in order
- Length in parentheses must match actual grid

Example:
```markdown
## Across

1. Feline pet (3)
2. Article (1)
3. Tree in winter (3)
```

**Down Clues** (`## Down`)
- Same format as across clues
- Numbers correspond to grid positions

Example:
```markdown
## Down

1. Feline pet (3)
2. First letter (1)
3. Third letter (1)
```

### Clue Number Assignment

Numbers are automatically assigned based on grid positions:

1. A cell gets an across clue number if:
   - It's in the first column, OR
   - The cell to its left is black

2. A cell gets a down clue number if:
   - It's in the first row, OR
   - The cell above it is black

3. Clue numbers increment as you traverse the grid left-to-right, top-to-bottom

This means you can omit clue numbers from your markdown and let the parser assign them:

```markdown
## Across

Feline pet (3)
Article (1)
```

(Auto-numbering will be added in future versions)

## Complete Example

```markdown
# Simple 3x3

A basic crossword to get started.

## Grid

```
  1 2 3
1 C A T
2 A . .
3 T . .
```

## Across

1. Feline pet (3)
2. Article (1)
3. Beverage (3)

## Down

1. Feline pet (3)
2. First letter (1)
3. Beverage (3)

```

## Validation Rules

The parser validates:

1. **Grid consistency**
   - All rows have the same number of cells
   - Cell letters are valid (A-Z or .)

2. **Clue consistency**
   - Clue numbers match grid clue positions
   - Clue lengths match actual grid dimensions
   - All numbers are sequential

3. **Content validation**
   - At least one across and one down clue
   - Grid has at least one white cell
   - No orphaned answers (length > 1)

## Special Cases

### Floating Cells

Single-letter cells don't get clue numbers:
```
  1 2 3
1 A B C
2 . . .
3 D E F
```

- A, B, C form one across answer
- D, E, F form another across answer
- But the single cells in row 2 don't get numbers

### Large Grids

The format scales to large grids:
```
  1  2  3  4  5
1  A  B  C  D  E
2  F  .  G  .  H
3  I  J  .  K  L
```

Use consistent spacing for readability.

## Tips for Creating Puzzles

### 1. Use Consistent Spacing

```markdown
## Grid

```
  1 2 3
1 A B C
2 D . E
3 F G H
```
```

### 2. Keep Clue Lengths Accurate

Count carefully - the parser will validate:
```markdown
1. Feline pet (3)  ← ABC = 3 letters ✓
```

### 3. Use Meaningful Clues

```markdown
1. Small feline mammal (3)        ← Too long
1. Domestic feline (3)            ← Better
1. Feline pet (3)                 ← Good
1. Tabby, e.g. (3)                ← Creative
```

### 4. Balance Difficulty

Use varied clue difficulties for an engaging puzzle.

### 5. Document Sources

Add a note if using publicly-licensed content:
```markdown
# Puzzle Title

Created by John Doe, 2024
Based on public domain content
```

## Future Extensions

### Metadata Section

Planned for future versions:
```markdown
---
author: John Doe
date: 2024-01-01
difficulty: medium
theme: Animals
source: Original
---
```

### Themed Puzzles

Planned feature - mark certain answers as themed:
```markdown
[THEME] 1. Feline pet (3)
```

### Alternative Formats

Planned support for:
- **Across Lite (.txt)** - Industry standard
- **PUZ Format (.puz)** - Crossword application format
- **JSON** - For programmatic puzzle generation
- **XML** - For complex metadata

## Troubleshooting

### "Clue length mismatch"
- Count the actual cells in the grid for that clue
- Adjust the number in parentheses

### "Invalid grid"
- Ensure each row has the same number of cells
- Use dots (.) for black cells, letters for white cells
- Use consistent spacing

### "Clue not found"
- Ensure clue numbers match grid positions
- Check grid section for proper formatting
- Verify clues are in correct section (Across/Down)
