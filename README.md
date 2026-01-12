# xword

A cooperative crossword puzzle application with multiplayer support, multiple frontends, and user-defined puzzles.

## Features

- **User-defined puzzles** - Define crossword puzzles in Markdown format
- **Cooperative play** - Multiple players can solve the same puzzle together
- **Console TUI** - Beautiful terminal interface powered by Textual
- **Server mode** - Run a server for multiplayer sessions (`xword -s`)
- **Wikipedia integration** - Auto-generate clues from Wikipedia
- **Multiple frontends** - Console TUI (ready), Web/iOS/Android support (planned)
- **Easy hosting** - Simple CLI for spinning up a server

## Quick Start

### Installation

```bash
pip install -e .
```

### Running the CLI

```bash
# Start a puzzle server
xword -s --port 8000

# Play locally
xword play puzzles/simple.md

# Generate clues for a puzzle
xword generate-clues puzzles/simple.md
```

## Puzzle Format

Define crosswords in Markdown:

```markdown
# My First Crossword

## Grid
```
  1 2 3 4
1 C A T .
2 A . . .
3 T . . .
```

## Across
1. Domestic animal (3)
3. Feline pet (3)

## Down
1. Feline pet (3)
2. First letter (1)
```

## Architecture

### Core Components

- **Puzzle Engine** - Validate, solve, and manage crossword puzzles
- **Puzzle Parser** - Parse Markdown and other puzzle formats
- **Server** - FastAPI-based multiplayer game server with WebSocket support
- **TUI Client** - Textual-based terminal interface
- **Wikipedia Module** - Auto-generate clues from Wikipedia

### Data Flow

```
Client (TUI) <--WebSocket--> Server (FastAPI) <---> Puzzle Engine
                                  ^
                                  |
                             Database
```

## Project Structure

```
xword/
├── xword/
│   ├── core/           # Puzzle engine logic
│   ├── server/         # Server implementation
│   ├── tui/            # Terminal UI
│   ├── client/         # Client networking
│   ├── formats/        # Puzzle format parsers
│   ├── utils/          # Utility functions
│   └── cli.py          # CLI entry point
├── tests/              # Test suite
├── docs/               # Documentation
├── examples/           # Example puzzles
└── pyproject.toml      # Project configuration
```

## Development

### Install development dependencies

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest tests/
```

### Format and lint

```bash
black xword/ tests/
ruff check xword/ tests/
```

## Roadmap

- [x] Project setup and architecture
- [ ] Core puzzle engine
- [ ] Markdown puzzle parser
- [ ] Console TUI interface
- [ ] Server implementation
- [ ] Multiplayer support
- [ ] Wikipedia integration
- [ ] Web frontend
- [ ] Mobile apps (iOS/Android)
- [ ] Puzzle generation/hints
- [ ] User profiles and statistics

## License

MIT
