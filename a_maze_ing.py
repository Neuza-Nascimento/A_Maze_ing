#!/usr/bin/env python3
import sys
from platform import python_version

from pydantic import ValidationError

from mazegen import MazeGenerator
from parsing import parser

MAX_ARGS: int = 2


def main() -> None:
    if len(sys.argv) != MAX_ARGS:
        sys.stderr.write(f"Usage: python{python_version()} <{sys.argv[0]}>\n")
        return
    try:
        config = parser(sys.argv[1])
        maze = MazeGenerator(config)
        maze.generate()
        for row in maze.get_grid():
            sys.stdout.write(f"{row}\n")
    except ValidationError as e:
        error = e.errors()[0]["msg"]
        msg: str = error.removeprefix("Value error, ")
        sys.stderr.write(f"{msg}\n")
    except (FileNotFoundError, SyntaxError, ValueError) as e:
        sys.stderr.write(f"Error: {e}\n")


if __name__ == "__main__":
    main()
