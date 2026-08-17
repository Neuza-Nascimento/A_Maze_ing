import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen import MazeConfig


class MazeGenerator:
    def __init__(self, config: MazeConfig) -> None:
        self.config: MazeConfig = config
        self.width: int = config.width
        self.height: int = config.height
        self.center: tuple[int, int] = (
            int(self.width / 2),
            int(self.height / 2),
        )
        self.grid: list[list[int]] = []

        random.seed(config.seed)
        self._create_grid()

    def _create_grid(self) -> None:
        ex, ey = self.config.entry
        sx, sy = self.config.exit
        cx, cy = self.center
        for i in range(self.height):
            row: list[int] = []
            for j in range(self.width):
                if i == ey and j == ex:
                    row.append(0b0010)
                    continue
                if i == sy and j == sx:
                    row.append(0b0010)
                    continue
                if cy in {i, j} or cx in {j, i}:
                    row.append(0b0001)
                    continue
                row.append(0b0000)
            self.grid.append(row)

    def _42_pattern(self) -> None: ...

    def _solution_path(self) -> list[str]:
        from collections import deque
        from enum import Enum

        NORTH = 0b0001
        EAST = 0b0010
        SOUTH = 0b0100
        WEST = 0b1000

        DIRECTIONS: dict[int, tuple[int, int]] = {
            NORTH: (0, -1),
            EAST: (1, 0),
            SOUTH: (0, 1),
            WEST: (-1, 0)
        }

        DIR_LETTER: dict[int, str] = {
            NORTH: "N",
            EAST:  "E",
            SOUTH: "S",
            WEST:  "W"
        }

        queque: deque[tuple[tuple[int, int], list[any]]] = deque(
            [(self.config.entry, [])])

        walls_visited: set[tuple[int, int]] = {self.config.entry}

        while queque:
            position, path = queque.popleft()
            px, py = position

            if position == self.config.exit:
                return path

            for direction, (dx, dy) in DIRECTIONS.items():
                nx = dx + px
                ny = dy + py

                if nx < 0 or nx >= self.width:
                    continue

                if ny < 0 or ny >= self.height:
                    continue

                if (nx, ny) in walls_visited:
                    continue

                if self.grid[px][py] & direction:
                    continue

                walls_visited.add((nx, ny))
                queque.append((nx, ny), path + DIR_LETTER[direction])

        return []

    def output_res(self) -> None:
        with open("output.txt", "w"):
            for i in self.grid:
                for j in self.grid:
                    