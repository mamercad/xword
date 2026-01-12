# Xword Server Guide

The Xword Server is a FastAPI-based backend that enables multiplayer crossword puzzle gaming with real-time synchronization via WebSocket.

## Starting the Server

### Basic Usage

```bash
xword serve --port 8000 --host 0.0.0.0
```

### Advanced Options

```bash
# Bind to specific interface
xword serve --host localhost --port 8000

# Run with custom workers (for production)
uvicorn xword.server.app:app --host 0.0.0.0 --port 8000 --workers 4

# Run with auto-reload (development)
uvicorn xword.server.app:app --reload
```

## API Documentation

### Interactive API Docs

Once server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Server Status

**Endpoint**: `GET /health`

Check if server is running and get status:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "ok",
  "active_sessions": 2,
  "loaded_puzzles": 5,
  "active_connections": 3
}
```

## Puzzle Management

### List Loaded Puzzles

**Endpoint**: `GET /puzzles`

```bash
curl http://localhost:8000/puzzles
```

Response:
```json
{
  "puzzles": [
    {
      "id": "puzzle-123",
      "title": "Simple Crossword",
      "description": "A basic 3x3 puzzle",
      "grid_size": "3x3",
      "clues": 6
    }
  ]
}
```

### Load a Puzzle

**Endpoint**: `POST /puzzles`

Load puzzle content to the server:

```bash
curl -X POST http://localhost:8000/puzzles \
  -H "Content-Type: application/json" \
  -d '{
    "puzzle_name": "my-puzzle",
    "puzzle_content": "# My Puzzle\n\n## Grid\n..."
  }'
```

Response:
```json
{
  "puzzle_id": "my-puzzle",
  "title": "My Puzzle",
  "grid_size": "3x3",
  "status": "loaded"
}
```

### Get Puzzle Details

**Endpoint**: `GET /puzzles/{puzzle_id}`

```bash
curl http://localhost:8000/puzzles/my-puzzle
```

Response:
```json
{
  "id": "my-puzzle",
  "title": "My Puzzle",
  "description": "A custom crossword",
  "grid_size": "3x3",
  "across_clues": [
    {"number": 1, "text": "Domestic feline", "length": 3}
  ],
  "down_clues": [
    {"number": 1, "text": "Pet", "length": 3}
  ]
}
```

## Session Management

### Create a Session

**Endpoint**: `POST /sessions`

Start a new game session:

```bash
curl -X POST "http://localhost:8000/sessions?puzzle_id=my-puzzle&username=alice"
```

Response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "puzzle_id": "my-puzzle",
  "username": "alice",
  "status": "created"
}
```

### Get Session State

**Endpoint**: `GET /sessions/{session_id}`

Get current progress:

```bash
curl http://localhost:8000/sessions/550e8400-e29b-41d4-a716-446655440000
```

Response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "puzzle_id": "my-puzzle",
  "participants": ["alice", "bob"],
  "filled_cells": 5,
  "correct_cells": 4,
  "total_cells": 9,
  "is_completed": false,
  "time_elapsed": 120
}
```

## Gameplay API

### Submit Cell Entry

**Endpoint**: `POST /sessions/{session_id}/entry`

Enter a letter in a cell:

```bash
curl -X POST "http://localhost:8000/sessions/550e8400-e29b-41d4-a716-446655440000/entry" \
  -H "Content-Type: application/json" \
  -d '{"row": 0, "col": 0, "letter": "C"}'
```

Response:
```json
{
  "status": "ok",
  "row": 0,
  "col": 0,
  "letter": "C"
}
```

Clear a cell:
```bash
curl -X POST "http://localhost:8000/sessions/550e8400-e29b-41d4-a716-446655440000/entry" \
  -H "Content-Type: application/json" \
  -d '{"row": 0, "col": 0, "letter": null}'
```

### Check Puzzle

**Endpoint**: `POST /sessions/{session_id}/check`

Validate if puzzle is complete:

```bash
curl -X POST "http://localhost:8000/sessions/550e8400-e29b-41d4-a716-446655440000/check"
```

Response:
```json
{
  "is_complete": true,
  "message": "Puzzle solved!"
}
```

### Get Hint

**Endpoint**: `POST /sessions/{session_id}/hint`

Request a hint for a clue:

```bash
curl -X POST "http://localhost:8000/sessions/550e8400-e29b-41d4-a716-446655440000/hint" \
  -H "Content-Type: application/json" \
  -d '{"clue_number": 1, "direction": "across"}'
```

Response:
```json
{
  "hint": "C",
  "message": "Hint: C"
}
```

## WebSocket Multiplayer

### Connecting to Multiplayer

**Endpoint**: `WS /ws/{session_id}?username={username}`

```bash
wscat -c "ws://localhost:8000/ws/550e8400-e29b-41d4-a716-446655440000?username=alice"
```

### Message Types

#### Welcome
Sent on connection:
```json
{
  "type": "welcome",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "alice",
  "participants": ["alice", "bob"]
}
```

#### Cell Entry
Send entry update:
```json
{
  "type": "entry",
  "row": 0,
  "col": 0,
  "letter": "C"
}
```

Receive entry from other player:
```json
{
  "type": "entry",
  "username": "bob",
  "row": 1,
  "col": 1,
  "letter": "A"
}
```

#### Check Puzzle
Send check:
```json
{
  "type": "check"
}
```

Receive from other player:
```json
{
  "type": "check",
  "username": "bob",
  "is_complete": false
}
```

#### User Left
Notified when player disconnects:
```json
{
  "type": "user_left",
  "username": "bob"
}
```

#### Keep-Alive
Send ping:
```json
{
  "type": "ping"
}
```

Receive pong:
```json
{
  "type": "pong"
}
```

## Client Library

### Python Client

```python
from xword.client import XwordClient
import asyncio

async def main():
    client = XwordClient("http://localhost:8000")
    
    # Load puzzle
    result = await client.load_puzzle("simple", open("examples/simple.md").read())
    puzzle_id = result["puzzle_id"]
    
    # Create session
    session = await client.create_session(puzzle_id, "alice")
    
    # Submit entry
    await client.submit_entry(0, 0, "C")
    
    # Get hint
    hint = await client.get_hint(1, "across")
    
    # Check if complete
    result = await client.check_puzzle()
    
    # Cleanup
    await client.disconnect()

asyncio.run(main())
```

### Multiplayer Example

```python
async def on_entry(data):
    print(f"{data['username']} entered {data['letter']} at ({data['row']},{data['col']})")

async def on_check(data):
    status = "Solved!" if data['is_complete'] else "Still playing"
    print(f"{data['username']}: {status}")

client = XwordClient("http://localhost:8000")
await client.create_session("simple", "alice")

# Connect to multiplayer
asyncio.create_task(
    client.connect_multiplayer(
        on_entry=on_entry,
        on_check=on_check
    )
)

# Send entries
await client.send_entry(0, 0, "C")
await client.send_check()

await client.disconnect()
```

## Deployment

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "xword.server.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t xword-server .
docker run -p 8000:8000 xword-server
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  xword-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./puzzles:/app/puzzles
```

Run:
```bash
docker-compose up
```

### Production Setup

For production deployment:

1. **Use Gunicorn with multiple workers**:
   ```bash
   gunicorn xword.server.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

2. **Use Nginx as reverse proxy**:
   ```nginx
   upstream xword {
       server localhost:8000;
   }
   
   server {
       listen 80;
       server_name crossword.example.com;
       
       location / {
           proxy_pass http://xword;
       }
       
       location /ws {
           proxy_pass http://xword;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

3. **Enable HTTPS**:
   ```bash
   certbot --nginx -d crossword.example.com
   ```

4. **Use environment variables**:
   ```bash
   export XWORD_HOST=0.0.0.0
   export XWORD_PORT=8000
   uvicorn xword.server.app:app
   ```

## Performance Tuning

### Connection Limits
- Adjust WebSocket timeout: `--ws-ping-interval 20`
- Connection pool size: `--pool-size 10`

### Memory Management
- Session cleanup: Sessions auto-cleanup after 24 hours of inactivity
- Puzzle caching: Loaded puzzles stay in memory

### Database (Future)
- Implement PostgreSQL for session persistence
- Add Redis for session caching
- Implement background job queue

## Monitoring

### Metrics to Track
- Active sessions
- Active WebSocket connections
- Average game duration
- Puzzle completion rate
- Server response time

### Health Check Integration
```bash
# Kubernetes liveness probe
curl -f http://localhost:8000/health

# Monitoring script
watch -n 5 "curl http://localhost:8000/health | python -m json.tool"
```

## Troubleshooting

### Server Won't Start
- Check port is not in use: `lsof -i :8000`
- Verify Python version: `python3 --version` (need 3.10+)
- Check dependencies: `pip install -e ".[dev]"`

### WebSocket Connection Fails
- Ensure WebSocket support in proxy
- Check firewall allows connections
- Verify client uses correct URL format (`ws://` not `http://`)

### Sessions Not Persisting
- Currently sessions are in-memory only
- Use database backend for persistence (planned)

### Performance Issues
- Check active sessions: `/health` endpoint
- Monitor memory usage
- Consider deploying multiple server instances with load balancer

## API Reference Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | API info |
| GET | `/health` | Server health |
| GET | `/puzzles` | List puzzles |
| POST | `/puzzles` | Load puzzle |
| GET | `/puzzles/{id}` | Get puzzle |
| POST | `/sessions` | Create session |
| GET | `/sessions/{id}` | Get session |
| POST | `/sessions/{id}/entry` | Submit entry |
| POST | `/sessions/{id}/check` | Check puzzle |
| POST | `/sessions/{id}/hint` | Get hint |
| WS | `/ws/{id}` | Multiplayer |

## Next Steps

- See DEVELOPMENT.md for extending the server
- See TUI_GUIDE.md for client usage
- Check ROADMAP.md for planned features
