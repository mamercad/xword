"""Client for connecting to xword server."""

import asyncio
import json
from typing import Optional, Callable, Any
import httpx
import websockets


class XwordClient:
    """Client for Xword server communication."""

    def __init__(self, server_url: str = "http://localhost:8000"):
        """Initialize client with server URL."""
        self.server_url = server_url
        self.ws_url = server_url.replace("http", "ws")
        self.http_client = httpx.AsyncClient(base_url=self.server_url)
        self.websocket = None
        self.session_id = None
        self.username = None

    async def health_check(self) -> dict:
        """Check server health."""
        response = await self.http_client.get("/health")
        return response.json()

    async def list_puzzles(self) -> list:
        """Get list of available puzzles."""
        response = await self.http_client.get("/puzzles")
        data = response.json()
        return data.get("puzzles", [])

    async def load_puzzle(self, puzzle_name: str, puzzle_content: str) -> dict:
        """Load a puzzle on the server."""
        response = await self.http_client.post(
            "/puzzles",
            json={"puzzle_name": puzzle_name, "puzzle_content": puzzle_content},
        )
        return response.json()

    async def get_puzzle(self, puzzle_id: str) -> dict:
        """Get puzzle details."""
        response = await self.http_client.get(f"/puzzles/{puzzle_id}")
        return response.json()

    async def create_session(self, puzzle_id: str, username: str = "player") -> dict:
        """Create a new game session."""
        response = await self.http_client.post(
            "/sessions", params={"puzzle_id": puzzle_id, "username": username}
        )
        data = response.json()
        self.session_id = data.get("session_id")
        self.username = username
        return data

    async def get_session(self) -> dict:
        """Get current session state."""
        if not self.session_id:
            raise ValueError("No active session")
        response = await self.http_client.get(f"/sessions/{self.session_id}")
        return response.json()

    async def submit_entry(self, row: int, col: int, letter: Optional[str]) -> dict:
        """Submit a cell entry."""
        if not self.session_id:
            raise ValueError("No active session")
        response = await self.http_client.post(
            f"/sessions/{self.session_id}/entry",
            json={"row": row, "col": col, "letter": letter},
        )
        return response.json()

    async def check_puzzle(self) -> dict:
        """Check if puzzle is complete."""
        if not self.session_id:
            raise ValueError("No active session")
        response = await self.http_client.post(f"/sessions/{self.session_id}/check")
        return response.json()

    async def get_hint(self, clue_number: int, direction: str) -> dict:
        """Get a hint for a clue."""
        if not self.session_id:
            raise ValueError("No active session")
        response = await self.http_client.post(
            f"/sessions/{self.session_id}/hint",
            json={"clue_number": clue_number, "direction": direction},
        )
        return response.json()

    async def connect_multiplayer(
        self,
        on_entry: Optional[Callable[[dict], Any]] = None,
        on_check: Optional[Callable[[dict], Any]] = None,
        on_user_left: Optional[Callable[[dict], Any]] = None,
    ) -> None:
        """Connect to multiplayer WebSocket."""
        if not self.session_id or not self.username:
            raise ValueError("Must create session before connecting")

        ws_url = (
            f"{self.ws_url}/ws/{self.session_id}?username={self.username}"
        )

        async with websockets.connect(ws_url) as websocket:
            self.websocket = websocket

            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)

                    if data["type"] == "welcome":
                        print(
                            f"Connected as {data.get('username')} "
                            f"to session {data.get('session_id')}"
                        )
                    elif data["type"] == "entry" and on_entry:
                        on_entry(data)
                    elif data["type"] == "check" and on_check:
                        on_check(data)
                    elif data["type"] == "user_left" and on_user_left:
                        on_user_left(data)

                except websockets.exceptions.ConnectionClosed:
                    break

    async def send_entry(self, row: int, col: int, letter: Optional[str]) -> None:
        """Send a cell entry via WebSocket."""
        if not self.websocket:
            raise ValueError("Not connected to multiplayer")

        message = json.dumps(
            {"type": "entry", "row": row, "col": col, "letter": letter}
        )
        await self.websocket.send(message)

    async def send_check(self) -> None:
        """Send a check request via WebSocket."""
        if not self.websocket:
            raise ValueError("Not connected to multiplayer")

        message = json.dumps({"type": "check"})
        await self.websocket.send(message)

    async def disconnect(self) -> None:
        """Disconnect from multiplayer."""
        if self.websocket:
            await self.websocket.close()
        if self.http_client:
            await self.http_client.aclose()
