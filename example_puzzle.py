#!/usr/bin/env python3
"""Example script demonstrating crossword puzzle generation."""

from xword.core.generator import GridGenerator
from xword.formats.display import GridDisplay


def main():
    """Generate and display example crossword puzzle."""

    # Your clues and answers
    across_clues = [
        (1, "Feline predator", 3),  # CAT
        (3, "Ursine mammal", 4),  # BEAR
        (5, "Striped cat", 5),  # TIGER
    ]

    down_clues = [
        (2, "Big cat", 4),  # LION
        (3, "Woolly animal", 5),  # SHEEP
        (4, "Smooth operator", 3),  # CON
        (5, "Sleep sound", 5),  # SNORE
    ]

    answers = {
        1: "CAT",
        3: "BEAR",
        5: "TIGER",
        2: "LION",
        4: "SHEEP",  # Wait, this should be a 5-letter word
        6: "CON",
        7: "SNORE",
    }

    # Simpler example with matching clues
    simple_across = [
        (1, "Feline predator", 3),  # CAT
        (4, "Ursine mammal", 4),  # BEAR
    ]

    simple_down = [
        (1, "Big cat", 4),  # LION
        (2, "First letter", 1),  # A
        (3, "Beverage", 3),  # TEA
    ]

    simple_answers = {
        1: "CAT",
        4: "BEAR",
        2: "LION",
        3: "A",
        5: "TEA",
    }

    # Generate puzzle
    generator = GridGenerator()

    print("=" * 60)
    print("SIMPLE CROSSWORD EXAMPLE")
    print("=" * 60)
    print()

    try:
        puzzle = generator.generate_from_clues(
            title="Simple Puzzle",
            description="A basic crossword to demonstrate grid generation",
            across_clues=simple_across,
            down_clues=simple_down,
            answers=simple_answers,
        )

        print("Grid (with letters):")
        print(GridDisplay.display_grid(puzzle.grid))
        print()

        print("Grid (with clue numbers):")
        print(GridDisplay.display_grid_with_clues(puzzle))
        print()

        print("Full Puzzle:")
        print(GridDisplay.display_puzzle(puzzle))

    except Exception as e:
        print(f"Error generating puzzle: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
