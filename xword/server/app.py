"""FastAPI server for multiplayer crossword puzzles."""

import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from xword.core.models import PuzzleDefinition
from xword.core.puzzle import PuzzleEngine
from xword.formats.markdown import MarkdownParser

# ============================================================================
# Data Models for API
# ============================================================================


class PuzzleLoad(BaseModel):
    """Request to load a puzzle."""

    puzzle_name: str
    puzzle_content: str


class CellEntry(BaseModel):
    """Cell entry submission."""

    row: int
    col: int
    letter: str | None = None


class HintRequest(BaseModel):
    """Request for a hint."""

    clue_number: int
    direction: str  # "across" or "down"


# ============================================================================
# Global State
# ============================================================================

# Global puzzle engine instance
puzzle_engine = PuzzleEngine()

# Loaded puzzles: puzzle_id -> PuzzleDefinition
loaded_puzzles: dict[str, PuzzleDefinition] = {}

# Active WebSocket connections for multiplayer
active_connections: dict[str, list] = {}


# ============================================================================
# Lifecycle Management
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for app startup/shutdown."""
    # Startup
    print("Xword server started")
    yield
    # Shutdown
    print("Xword server shutdown")


app = FastAPI(
    title="Xword Server",
    description="Multiplayer crossword puzzle server",
    version="0.1.0",
    lifespan=lifespan,
)


# ============================================================================
# REST API Endpoints
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Xword Server API",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "puzzles": "/puzzles",
            "sessions": "/sessions",
            "ws": "/ws/{session_id}",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "active_sessions": len(puzzle_engine.sessions),
        "loaded_puzzles": len(loaded_puzzles),
        "active_connections": sum(len(conns) for conns in active_connections.values()),
    }


# ============================================================================
# Puzzle Management Endpoints
# ============================================================================


@app.get("/puzzles")
async def list_puzzles():
    """List all loaded puzzles."""
    return {
        "puzzles": [
            {
                "id": pid,
                "title": p.title,
                "description": p.description,
                "grid_size": f"{p.grid.rows}x{p.grid.cols}",
                "clues": len(p.across_clues) + len(p.down_clues),
            }
            for pid, p in loaded_puzzles.items()
        ]
    }


@app.post("/puzzles")
async def load_puzzle(puzzle: PuzzleLoad):
    """Load a puzzle from markdown content."""
    try:
        puzzle_def = MarkdownParser.parse(puzzle.puzzle_content)
        puzzle_id = puzzle.puzzle_name or str(uuid.uuid4())
        loaded_puzzles[puzzle_id] = puzzle_def

        return {
            "puzzle_id": puzzle_id,
            "title": puzzle_def.title,
            "grid_size": f"{puzzle_def.grid.rows}x{puzzle_def.grid.cols}",
            "status": "loaded",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse puzzle: {e!s}")


@app.get("/puzzles/{puzzle_id}")
async def get_puzzle(puzzle_id: str):
    """Get puzzle details."""
    if puzzle_id not in loaded_puzzles:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    puzzle = loaded_puzzles[puzzle_id]
    return {
        "id": puzzle_id,
        "title": puzzle.title,
        "description": puzzle.description,
        "grid_size": f"{puzzle.grid.rows}x{puzzle.grid.cols}",
        "across_clues": [
            {"number": c.number, "text": c.text, "length": c.length}
            for c in puzzle.across_clues
        ],
        "down_clues": [
            {"number": c.number, "text": c.text, "length": c.length}
            for c in puzzle.down_clues
        ],
    }


# ============================================================================
# Session Management Endpoints
# ============================================================================


@app.post("/sessions")
async def create_session(puzzle_id: str, username: str = "anonymous"):
    """Create a new puzzle session."""
    if puzzle_id not in loaded_puzzles:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    puzzle = loaded_puzzles[puzzle_id]
    session_id = str(uuid.uuid4())

    try:
        session = puzzle_engine.create_session(session_id, puzzle, username)
        active_connections[session_id] = []

        return {
            "session_id": session_id,
            "puzzle_id": puzzle_id,
            "username": username,
            "status": "created",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {e!s}")


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session state."""
    session = puzzle_engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Count filled and correct cells
    filled = 0
    correct = 0
    for cell in session.grid.cells.values():
        if cell.user_entry:
            filled += 1
            if cell.is_correct():
                correct += 1

    return {
        "session_id": session_id,
        "puzzle_id": session.puzzle_id,
        "participants": list(session.participants),
        "filled_cells": filled,
        "correct_cells": correct,
        "total_cells": len(session.grid.cells),
        "is_completed": session.is_completed,
        "time_elapsed": int(
            session.completed_at - session.start_time
            if session.completed_at
            else __import__("time").time() - session.start_time
        ),
    }


# ============================================================================
# Game Play Endpoints
# ============================================================================


@app.post("/sessions/{session_id}/entry")
async def submit_entry(session_id: str, entry: CellEntry):
    """Submit a cell entry."""
    if session_id not in puzzle_engine.sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    success = puzzle_engine.set_cell_entry(
        session_id, entry.row, entry.col, entry.letter
    )

    if not success:
        raise HTTPException(status_code=400, detail="Invalid entry")

    return {"status": "ok", "row": entry.row, "col": entry.col, "letter": entry.letter}


@app.post("/sessions/{session_id}/check")
async def check_puzzle(session_id: str):
    """Check if puzzle is solved."""
    if session_id not in puzzle_engine.sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    is_complete = puzzle_engine.check_puzzle(session_id)

    return {
        "is_complete": is_complete,
        "message": "Puzzle solved!" if is_complete else "Not yet complete",
    }


@app.post("/sessions/{session_id}/hint")
async def get_hint(session_id: str, hint_request: HintRequest):
    """Get a hint for a clue."""
    session = puzzle_engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Find the clue
    clues = (
        session.puzzle.across_clues
        if hint_request.direction.lower() == "across"
        else session.puzzle.down_clues
    )

    clue = None
    for c in clues:
        if c.number == hint_request.clue_number:
            clue = c
            break

    if not clue:
        raise HTTPException(status_code=404, detail="Clue not found")

    hint_letter = puzzle_engine.get_hint(session_id, clue)

    return {"hint": hint_letter, "message": f"Hint: {hint_letter}" if hint_letter else "No more hints"}


# ============================================================================
# WebSocket Handlers (Multiplayer Real-Time)
# ============================================================================


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, username: str = "player"):
    """WebSocket endpoint for real-time multiplayer."""
    session = puzzle_engine.get_session(session_id)
    if not session:
        await websocket.close(code=4004, reason="Session not found")
        return

    await websocket.accept()

    # Add participant
    puzzle_engine.add_participant(session_id, username)

    if session_id not in active_connections:
        active_connections[session_id] = []

    active_connections[session_id].append(websocket)

    try:
        # Send welcome message
        await websocket.send_json(
            {
                "type": "welcome",
                "session_id": session_id,
                "username": username,
                "participants": list(session.participants),
            }
        )

        while True:
            data = await websocket.receive_json()

            if data["type"] == "entry":
                # Cell entry from user
                puzzle_engine.set_cell_entry(
                    session_id, data["row"], data["col"], data.get("letter")
                )

                # Broadcast to all connected clients
                message = {
                    "type": "entry",
                    "username": username,
                    "row": data["row"],
                    "col": data["col"],
                    "letter": data.get("letter"),
                }

                for connection in active_connections[session_id]:
                    try:
                        await connection.send_json(message)
                    except:
                        pass

            elif data["type"] == "check":
                # Check puzzle
                is_complete = puzzle_engine.check_puzzle(session_id)

                message = {
                    "type": "check",
                    "is_complete": is_complete,
                    "username": username,
                }

                for connection in active_connections[session_id]:
                    try:
                        await connection.send_json(message)
                    except:
                        pass

            elif data["type"] == "ping":
                # Keep-alive ping
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        active_connections[session_id].remove(websocket)

        # Notify others that user disconnected
        if active_connections[session_id]:
            for connection in active_connections[session_id]:
                try:
                    await connection.send_json(
                        {"type": "user_left", "username": username}
                    )
                except:
                    pass

