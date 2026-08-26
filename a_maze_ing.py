#!/usr/bin/env python3

"""A_Maze_Ing main file."""

import sys
from platform import python_version

from pydantic import ValidationError

from mazegen import MazeGenerator, MazeVisualizer
from parsing import parser

MAX_ARGS: int = 2


def main() -> None:
    """Start.

    Handles parsing of the command line argument,
    internal configuration and verification of the maze,
    executes the maze generation and maze solving, as well
    as the maze visual display.

    Any possible erros that come from the config file
    are handled here as well.
    """
    if len(sys.argv) != MAX_ARGS:
        sys.stderr.write(f"Usage: python{python_version()} <{sys.argv[0]}>\n")
        return
    try:
        config = parser(sys.argv[1])
        maze = MazeGenerator(config)
        maze.generate()
    except ValidationError as e:
        error = e.errors()[0]["msg"]
        msg: str = error.removeprefix("Value error, ")
        sys.stderr.write(f"{msg}\n")
        sys.exit(1)
    except (FileNotFoundError, SyntaxError, ValueError) as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
    if not maze.solve():
        sys.exit(1)
    visu = MazeVisualizer(maze)
    visu.render()


if __name__ == "__main__":
    main()
