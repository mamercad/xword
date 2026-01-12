# Xword Architecture

## Overview

Xword is designed as a modular system with clear separation of concerns, allowing it to support multiple frontends and deployment configurations.

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
├─────────────────┬─────────────────┬──────────────────────────┤
│  Console TUI    │  Web Frontend    │  Mobile Apps (iOS/etc)  │
│  (Textual)      │  (React)         │  (React Native/etc)     │
└────────┬────────┴────────┬────────┴──────────────┬───────────┘
         │                 │                       │
         └─────────────────┴───────────┬───────────┘
                                      │
                          ┌───────────┴──────────┐
                          │  Network/Protocol    │
                          │  (WebSocket, HTTP)   │
                          └───────────┬──────────┘
                                      │
         ┌────────────────────────────┴────────────────────────┐
         │              Server Layer (FastAPI)                 │
         │  ┌──────────────────────────────────────────────┐   │
         │  │         Game Logic / Routing                 │   │
         │  │  - Puzzle endpoints                          │   │
         │  │  - Session management                        │   │
         │  │  - WebSocket handlers                        │   │
         │  └──────────────────────────────────────────────┘   │
         └────────────────────────────────────────────────────┘
                                      │
                                      │
         ┌────────────────────────────┴────────────────────────┐
         │           Core Engine Layer                         │
         │  ┌──────────────────────────────────────────────┐   │
         │  │      PuzzleEngine                            │   │
         │  │  - Session management                        │   │
         │  │  - Validation logic                          │   │
         │  │  - Clue mapping                              │   │
         │  │  - Completion checking                       │   │
         │  └──────────────────────────────────────────────┘   │
         │  ┌──────────────────────────────────────────────┐   │
         │  │      Puzzle Models                           │   │
         │  │  - Cell, Clue, Grid                          │   │
         │  │  - PuzzleDefinition, PuzzleSession           │   │
         │  └──────────────────────────────────────────────┘   │
         │  ┌──────────────────────────────────────────────┐   │
         │  │      Format Parsers                          │   │
         │  │  - MarkdownParser (primary)                  │   │
         │  │  - AcrossLiteParser (planned)                │   │
         │  │  - PUZParser (planned)                       │   │
         │  └──────────────────────────────────────────────┘   │
         └────────────────────────────────────────────────────┘
                                      │
         ┌────────────────────────────┴────────────────────────┐
         │           Data Storage Layer                        │
         │  - In-memory sessions (MVP)                         │
         │  - SQLite/PostgreSQL (planned)                      │
         │  - Puzzle library storage                           │
         └────────────────────────────────────────────────────┘
```

## Components

### Core Engine (`xword/core/`)

#### Models (`models.py`)

**Cell**
- Represents a single cell in a crossword grid
- Properties: position, letter (solution), user entry, black cell flag
- Methods: validation, correctness checking

**Clue**
- Represents an across/down clue
- Properties: number, direction, text, positions, answer
- Maps to cells in the grid

**Grid**
- 2D grid of cells
- Sparse representation using dictionary for memory efficiency
- Methods: cell access, iteration

**PuzzleDefinition**
- Complete puzzle specification
- Properties: title, description, grid, clues, difficulty
- Methods: serialization, clue access

**PuzzleSession**
- Active playing session
- Properties: puzzle reference, working grid, participants, timing
- Tracks user progress and multiplayer state

#### Engine (`puzzle.py`)

**PuzzleEngine**
- Central game logic coordinator
- Session management (create, retrieve, update)
- Cell entry validation
- Puzzle completion checking
- Hint generation
- Participant management

### Format Parsers (`xword/formats/`)

**MarkdownParser** (Primary format)
- Human-readable markdown-based format
- Grid definition in ASCII table
- Clues in standard markdown lists
- Easy to version control and edit

Format example:
```markdown
# Puzzle Title

## Grid
```
  1 2 3
1 C A T
2 A . .
3 T . .
```

## Across
1. Definition (3)

## Down
1. Definition (3)
```

### Server (`xword/server/`)

**FastAPI Application**
- RESTful API for puzzle operations
- WebSocket endpoints for real-time multiplayer
- Session management
- User authentication (planned)
- Persistence layer integration

Key endpoints (planned):
- `GET /puzzles` - List available puzzles
- `GET /puzzles/{id}` - Get puzzle definition
- `POST /sessions` - Create new session
- `GET /sessions/{id}` - Get session state
- `WS /sessions/{id}/join` - Join multiplayer session
- `WS /sessions/{id}/play` - Real-time game updates

### TUI Client (`xword/tui/`)

**Textual Application**
- Terminal-based interactive interface
- Grid display with clue panel
- Real-time validation feedback
- Keyboard navigation
- Multiplayer presence indicator

### Client Library (`xword/client/`)

**ServerClient** (planned)
- Handles server communication
- WebSocket client
- Automatic reconnection
- Event dispatching

## Data Flow

### Puzzle Loading

```
Markdown File
     ↓
MarkdownParser.parse()
     ↓
PuzzleDefinition
     ↓
PuzzleEngine.create_session()
     ↓
PuzzleSession (with empty user grid)
     ↓
Client displays puzzle
```

### User Entry

```
User types letter
     ↓
TUI captures keystroke
     ↓
Client validates locally
     ↓
PuzzleEngine.set_cell_entry()
     ↓
Server broadcasts to other participants
     ↓
All clients update display
```

### Completion Check

```
User submits puzzle
     ↓
PuzzleEngine.check_puzzle()
     ↓
Validate all cells
     ↓
If complete:
  - Mark session as complete
  - Record completion time
  - Broadcast to participants
```

## State Management

### Local Session State (Client)

```python
{
  "puzzle_id": "simple-1",
  "grid": {
    (0, 0): {"letter": "C", "user_entry": "C", "is_correct": true},
    ...
  },
  "current_clue": {"number": 1, "direction": "across"},
  "time_elapsed": 125
}
```

### Server Session State

```python
{
  "puzzle_id": "simple-1",
  "puzzle": PuzzleDefinition,
  "grid": Grid (with user entries),
  "participants": ["user1", "user2"],
  "start_time": 1234567890.0,
  "is_completed": false,
  "last_updated": 1234567900.0
}
```

## Communication Protocol

### Single-Player (Local)

1. Load puzzle file from filesystem
2. Create session in local PuzzleEngine
3. Display grid and accept input
4. Validate entries locally
5. Save progress to file (planned)

### Multiplayer (Network)

```
Client 1              Server              Client 2
  │                     │                   │
  ├─ Connect ──────────>│                   │
  │                     │<──── Connect ─────┤
  │                     │                   │
  ├─ Load puzzle ──────>│                   │
  │                     │<──── Load ────────┤
  │                     │                   │
  ├─ Enter letter ─────>│<─── update ───────┤
  │                     │                   │
  │<──── update ────────┤ ──── update ─────>│
  │                     │                   │
  └─ Display update ────┘ ─── Display ─────┘
```

## Future Extensibility

### Plugin Architecture

Format parsers can be registered at runtime:
```python
engine.register_parser("puz", PUZParser)
engine.register_parser("across_lite", AcrossLiteParser)
```

### Multiple Backend Support

Database abstraction layer allows:
- In-memory (current)
- SQLite
- PostgreSQL
- Firebase (cloud)

### Frontend Implementations

- Console TUI (Textual) ✓
- Web (React + WebSocket)
- Mobile (React Native)
- Terminal GUIs (curses, brick)

### Puzzle Sources

- User-defined (markdown files)
- Wikipedia-generated clues
- Public puzzle APIs
- Community puzzle library

## Performance Considerations

### Grid Representation

Uses sparse dictionary representation:
```python
cells: Dict[Tuple[int, int], Cell]
```

Benefits:
- O(1) cell access
- Memory efficient for large sparse grids
- Easy iteration

### Session Management

Sessions stored in-memory for MVP:
```python
sessions: Dict[str, PuzzleSession]
```

Scaling strategy:
1. Redis for distributed sessions
2. Database for persistence
3. Cache invalidation policies

### Clue Mapping

Precomputed during puzzle loading:
- Cell-to-clue mapping
- Clue-to-cell lists
- Validation caches

## Security Considerations

- User input sanitization (planned)
- Rate limiting on server (planned)
- WebSocket authentication (planned)
- Puzzle validation on load
- No arbitrary code execution

## Testing Strategy

- Unit tests for core engine
- Integration tests for puzzle loading
- E2E tests for multiplayer flow
- Fixture puzzles for regression testing
