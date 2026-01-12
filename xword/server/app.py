"""FastAPI server for multiplayer crossword puzzles."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from xword.core.puzzle import PuzzleEngine

# Global puzzle engine instance
puzzle_engine = PuzzleEngine()


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


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Xword Server API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


# WebSocket endpoints for multiplayer
# TODO: Implement WebSocket handlers for real-time puzzle updates
