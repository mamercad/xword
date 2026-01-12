# Xword Quick Start Guide

Get up and running with xword in 5 minutes!

## Installation

### Using pip (Coming Soon)
```bash
pip install xword-puzzle
```

### From source (Current)
```bash
git clone https://github.com/mamercad/xword.git
cd xword
python3 -m pip install -e .
```

## Basic Usage

### View a Puzzle

See puzzle information without playing:

```bash
xword show examples/simple.md
```

Output:
```
Title: Simple Crossword
Description: A basic 3x3 crossword puzzle to demonstrate the format.
Grid size: 3x3
Across clues: 3
Down clues: 3

Across:
  1. Domestic feline (3)
  2. Article (1)
  3. Beverage (3)

Down:
  1. Feline pet (3)
  2. First letter (1)
  3. Beverage (3)
```

### Play a Puzzle

Start the interactive puzzle game (TUI - coming soon):

```bash
xword play examples/simple.md
```

The interface will display:
- The crossword grid with numbered clues
- Clue panel showing all across/down clues
- Input area for entering letters
- Keyboard shortcuts for navigation

### Run a Server

Start a server for multiplayer games:

```bash
xword serve --port 8000
```

This starts the server on `localhost:8000`. Other players can connect using the client:

```bash
xword play --server localhost:8000
```

## Create Your Own Puzzle

### Basic Structure

Create a file `my_puzzle.md`:

```markdown
# My First Crossword

A fun puzzle about my favorite things.

## Grid

```
  1 2 3 4 5
1 C A T . .
2 A . . . .
3 T . . . .
4 . . . . .
5 . . . . .
```

## Across

1. Domestic feline (3)

## Down

1. Feline pet (3)
```

### Test Your Puzzle

```bash
xword show my_puzzle.md
```

If there are any parsing errors, fix them and try again.

### Play Your Puzzle

```bash
xword play my_puzzle.md
```

## Format Guide

### Grid Section

- Use spaces to separate columns
- Use numbers at the top and left for reference
- Letters are white cells (enter answer letters here)
- Dots (.) are black cells (blocked squares)

```
  1 2 3
1 A B C
2 D . E
3 F G H
```

This creates:
- Row 1: ABC
- Row 2: D_E (where _ is a blocked square)
- Row 3: FGH

### Clues Section

Format: `NUMBER. Clue text (LENGTH)`

```markdown
## Across

1. First across clue (3)
2. Second across clue (5)

## Down

1. First down clue (4)
2. Second down clue (3)
```

**Important**: The length in parentheses must match the number of cells in the grid!

## Examples

Several example puzzles are included:

```bash
# Simple 3x3 starter puzzle
xword show examples/simple.md

# Animal-themed puzzle
xword show examples/animals.md

# Quick puzzle for learning
xword show examples/quick.md
```

## Common Commands

```bash
# Get help
xword --help

# Show specific command help
xword play --help
xword serve --help

# Show puzzle details
xword show examples/simple.md

# Start server on custom port
xword serve -p 9000

# Play locally
xword play examples/simple.md

# Join multiplayer game
xword play --server example.com:8000
```

## Troubleshooting

### "Grid not found" error
Make sure your puzzle has a `## Grid` section with a code block.

### "Clue length mismatch" error
Count the cells in the grid for that clue and fix the number in parentheses.

### "Clue number not found" error
Ensure all clue numbers match the grid layout. Clues are numbered from top-left:
- First across clue starts at top-left
- First down clue also starts at top-left
- Numbers increment left-to-right, top-to-bottom

### Grid looks wrong
Check spacing in your markdown code block. Use consistent spacing for all columns:
```markdown
```
  1 2 3
1 A B C
2 D . E
3 F G H
```
(Don't mix tabs and spaces)
```

## Next Steps

1. **Create more puzzles** - Build a personal collection
2. **Share puzzles** - Submit to examples folder
3. **Play multiplayer** - Use `xword serve` and invite friends
4. **Contribute** - See CONTRIBUTING.md to help develop features

## Features Status

### Current (MVP)
✅ Puzzle format and parser
✅ CLI interface
✅ Single puzzle viewing
✅ Example puzzles

### Coming Soon
🔄 Console TUI gameplay
🔄 Server with multiplayer
🔄 Hints and validation

### Planned
📋 Web frontend
📋 Mobile apps
📋 Wikipedia clue generation
📋 Community puzzle library

## Documentation

- **PUZZLE_FORMAT.md** - Detailed format specification
- **ARCHITECTURE.md** - System design and components
- **DEVELOPMENT.md** - Setup and development guide
- **CONTRIBUTING.md** - How to contribute
- **ROADMAP.md** - Future development plan

## Getting Help

- **Issues**: Report bugs on GitHub
- **Discussions**: Ask questions in GitHub discussions
- **Docs**: Check documentation folder
- **Examples**: Study example puzzles

## Contributing

We'd love your help! See CONTRIBUTING.md for:
- How to report bugs
- How to suggest features
- How to contribute code
- Creating example puzzles

## License

Xword is MIT licensed. See LICENSE file for details.

---

Happy puzzle solving! 🎉
