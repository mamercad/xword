# Xword Terminal UI Guide

The Xword Terminal UI (TUI) is a full-featured crossword puzzle game interface built with Textual.

## Starting the Game

```bash
xword play examples/simple.md
```

This launches the interactive puzzle interface in your terminal.

## Interface Layout

The TUI interface has three main sections:

```
┌─────────────────────────────────────────────────────────────┐
│  Xword - Simple Crossword                           Help    │
├──────────────────────────────┬──────────────────────────────┤
│                              │                              │
│      Crossword Grid          │      Clue Panel             │
│                              │                              │
│   1  2  3                    │  ACROSS:                    │
│ 1 C  A  T                    │  1. Domestic feline (3)     │
│ 2 A  .  .                    │  2. Article (1)             │
│ 3 T  .  .                    │                              │
│                              │  DOWN:                      │
│                              │  1. Feline pet (3)          │
│                              │  2. First letter (1)        │
│                              │                              │
├──────────────────────────────┴──────────────────────────────┤
│ Simple Crossword | Solved: 0/6 | ↑↓←→ Navigate | Q Quit    │
└──────────────────────────────────────────────────────────────┘
```

### Grid (Left Side)
- Displays the crossword puzzle
- Highlighted cell shows current position
- Green letters indicate correct entries
- Dots (.) represent blocked cells
- Numbers indicate clue starts

### Clue Panel (Right Side)
- Shows all across and down clues
- Highlighted clue corresponds to current cell
- Clue format: `Number. Text (Length)`

### Status Bar (Bottom)
- Shows puzzle title and progress
- Displays available keyboard commands
- Shows current statistics

## Keyboard Shortcuts

### Navigation
| Key | Action |
|-----|--------|
| `↑` or `W` | Move cursor up |
| `↓` or `S` | Move cursor down |
| `←` or `A` | Move cursor left |
| `→` or `D` | Move cursor right |
| `Tab` | Switch between across/down |

### Editing
| Key | Action |
|-----|--------|
| `A-Z` | Enter letter in current cell |
| `Backspace` | Clear current cell |
| `Delete` | Clear current cell |
| `0-9` | Jump to cell number (planned) |

### Game Controls
| Key | Action |
|-----|--------|
| `Ctrl+H` | Get hint (reveal one letter) |
| `Ctrl+C` | Check puzzle (validate all entries) |
| `Ctrl+S` | Save progress to file |
| `Ctrl+U` | Undo last entry |
| `Ctrl+R` | Redo last entry |
| `Ctrl+?` | Show help screen |
| `Q` | Quit game (with save prompt) |

## Playing the Game

### 1. Starting Out

When you launch the game, the cursor starts at the first white cell (top-left).

### 2. Reading Clues

Check the clue panel on the right for:
- **Current clue**: Highlighted row in clue panel
- **Clue number**: Matches the number at that grid position
- **Clue text**: Description to help you solve
- **Length**: Number of cells in parentheses

### 3. Entering Answers

1. Navigate to a cell with arrow keys
2. Type a letter (A-Z)
3. The cursor auto-advances to the next cell
4. The cell turns green when correctly filled

### 4. Getting Help

- **Hint**: Press `Ctrl+H` to reveal one letter in the current clue
- **Check**: Press `Ctrl+C` to validate all entries without submitting

### 5. Completing the Puzzle

Once you've filled all cells correctly:

1. The interface shows green for all correct answers
2. Press `Ctrl+C` to officially complete the puzzle
3. Completion time and statistics are recorded

### 6. Saving Progress

Your progress is automatically saved every 30 seconds. You can also:

- Press `Ctrl+S` to manually save
- Quit with `Q` to save before exiting
- Resume with `xword resume puzzle-name`

## Tips & Tricks

### Navigation Tips
- Use arrow keys for precise movement
- Tab switches between across and down clues for current cell
- Use `0-9` to jump directly to a clue number (if implemented)

### Solving Tips
- Start with longer clues (more constraints)
- Look for common crossword patterns
- Use hints sparingly for better scores
- Check before submitting to catch errors

### Performance Tips
- Larger puzzles may take longer to render
- Press `Ctrl+L` to redraw screen if display glitches
- Works best in terminal with at least 80x24 characters

## Color Legend

| Color | Meaning |
|-------|---------|
| White | Cell waiting for entry |
| Green | Correct answer |
| Yellow | Partially correct (1-9 letters) |
| Black | Blocked/empty cell |
| Cyan | Current active clue |

## Troubleshooting

### Cursor not moving
- Ensure you're using arrow keys, not WASD
- Check that cursor isn't at puzzle boundary
- Try pressing `Ctrl+L` to refresh display

### Characters not appearing
- Make sure terminal supports UTF-8
- Check terminal size is at least 80x24
- Try resizing terminal window

### Game freezes
- Press `Ctrl+C` to interrupt
- Re-launch with `xword play puzzle.md`
- Check puzzle file for syntax errors with `xword show puzzle.md`

### Progress lost
- Check if save file exists
- Game auto-saves every 30 seconds
- Resume previous game with `xword resume`

## Accessibility Features

### Screen Reader Support (Planned)
- Grid description
- Clue reading
- Status announcements

### Keyboard-Only Navigation
- All controls available via keyboard
- No mouse required
- Tab navigation through interface

### High Contrast Mode
- `--high-contrast` flag for better visibility
- Works with terminal themes

### Text Size
- Adjust terminal font size for readability
- TUI automatically adapts to window size

## Advanced Features

### Custom Themes (Planned)
```bash
xword play puzzle.md --theme dark
xword play puzzle.md --theme light
xword play puzzle.md --theme high-contrast
```

### Statistics Tracking
The TUI tracks:
- Time spent playing
- Hints used
- Errors made
- Accuracy percentage
- Completion status

### Multiplayer Mode (Planned)
```bash
xword play --server localhost:8000 puzzle.md
```

Connect to a multiplayer session and see other players' progress in real-time.

## Performance

### Typical Performance
- **Load time**: <100ms for puzzles up to 20x20
- **Frame rate**: 60 FPS for smooth navigation
- **Memory usage**: <20MB for typical puzzles

### Large Puzzles (>20x20)
- Rendering may be slower
- Consider using smaller terminal or zooming out
- Complex puzzles might benefit from custom grid rendering

## Extending the TUI

The TUI is built with Textual, making it easy to extend:

```python
from xword.tui.app import XwordApp
from textual.widgets import Static

class CustomWidget(Static):
    def render(self):
        return "Custom content"
```

See `docs/DEVELOPMENT.md` for extending the TUI.

## Reporting Issues

Found a bug or have a feature request?

1. Check if it's listed in ROADMAP.md
2. Open an issue on GitHub with:
   - Terminal type and size
   - Puzzle file (if relevant)
   - Steps to reproduce
   - Expected vs actual behavior

## Next Steps

- **Play a puzzle**: `xword play examples/simple.md`
- **Create your own**: See PUZZLE_FORMAT.md
- **Customize settings**: Edit xword config file (planned)
- **Join multiplayer**: See server setup guide (planned)
