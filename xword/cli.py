"""Command-line interface for xword."""

import argparse
import sys
from pathlib import Path

from xword.formats.markdown import MarkdownParser


def load_puzzle(puzzle_path: str):
    """Load a puzzle from a file."""
    path = Path(puzzle_path)
    if not path.exists():
        print(f"Error: Puzzle file not found: {puzzle_path}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text()
    puzzle = MarkdownParser.parse(content)
    return puzzle


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Xword - Cooperative Crossword Puzzles")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Play command
    play_parser = subparsers.add_parser("play", help="Play a puzzle in TUI mode")
    play_parser.add_argument("puzzle", help="Path to puzzle file (markdown)")

    # Server command
    server_parser = subparsers.add_parser("serve", help="Run a multiplayer server")
    server_parser.add_argument("-p", "--port", type=int, default=8000, help="Port to listen on")
    server_parser.add_argument("-H", "--host", default="0.0.0.0", help="Host to bind to")

    # Generate clues command
    generate_parser = subparsers.add_parser("generate-clues", help="Generate clues from Wikipedia")
    generate_parser.add_argument("puzzle", help="Path to puzzle file")
    generate_parser.add_argument("-o", "--output", help="Output file (default: overwrite input)")

    # Show puzzle command
    show_parser = subparsers.add_parser("show", help="Display puzzle information")
    show_parser.add_argument("puzzle", help="Path to puzzle file")

    args = parser.parse_args()

    if args.command == "play":
        play_puzzle(args.puzzle)
    elif args.command == "serve":
        run_server(args.host, args.port)
    elif args.command == "generate-clues":
        generate_clues(args.puzzle, args.output)
    elif args.command == "show":
        show_puzzle(args.puzzle)
    else:
        parser.print_help()
        sys.exit(0)


def play_puzzle(puzzle_path: str):
    """Play a puzzle in TUI mode."""
    puzzle = load_puzzle(puzzle_path)

    try:
        from xword.tui.app import XwordApp

        app = XwordApp(puzzle)
        app.run()
    except ImportError:
        print("Error: TUI not yet implemented", file=sys.stderr)
        sys.exit(1)


def run_server(host: str, port: int):
    """Run the multiplayer server."""
    try:
        import uvicorn

        from xword.server.app import app

        print(f"Starting xword server on {host}:{port}")
        print("Connect with: xword play ws://localhost:{port}")
        uvicorn.run(app, host=host, port=port)
    except ImportError:
        print("Error: Server not yet implemented", file=sys.stderr)
        sys.exit(1)


def generate_clues(puzzle_path: str, output_path: str = None):
    """Generate clues from Wikipedia for a puzzle."""
    puzzle = load_puzzle(puzzle_path)

    try:
        from xword.utils.wikipedia import WikipediaClueGenerator

        generator = WikipediaClueGenerator()
        # This would implement clue generation
        print("Clue generation not yet implemented", file=sys.stderr)
    except ImportError:
        print("Error: Wikipedia module not available", file=sys.stderr)
        sys.exit(1)


def show_puzzle(puzzle_path: str):
    """Display puzzle information."""
    puzzle = load_puzzle(puzzle_path)

    print(f"Title: {puzzle.title}")
    print(f"Description: {puzzle.description}")
    print(f"Grid size: {puzzle.grid.rows}x{puzzle.grid.cols}")
    print(f"Across clues: {len(puzzle.across_clues)}")
    print(f"Down clues: {len(puzzle.down_clues)}")
    print()

    print("Across:")
    for clue in puzzle.across_clues:
        print(f"  {clue.number}. {clue.text} ({clue.length})")

    print("\nDown:")
    for clue in puzzle.down_clues:
        print(f"  {clue.number}. {clue.text} ({clue.length})")


if __name__ == "__main__":
    main()
