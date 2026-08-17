import random
from typing import TYPE_CHECKING

from magic_values import P42, MagicValues

if TYPE_CHECKING:
    from mazegen import MazeConfig


class MazeGenerator:
    def __init__(self, config: MazeConfig) -> None:
        self.config: MazeConfig = config
        self.width: int = config.width
        self.height: int = config.height
        self.grid: list[list[int]] = []
        self.blocked: set = set()
        random.seed(config.seed)
        self._create_grid()

    def _create_grid(self) -> None:
        n: int = MagicValues.NORTH.value
        for _ in range(self.height):
            row: list[int] = [n for _ in range(self.width)]
            self.grid.append(row)
        self._42_pattern()

    def _42_pattern(self) -> bool:
        center_x = (self.width // 2) - 5
        center_y = (self.height // 2) - 4
        for i in range(1, self.height - 1):
            row = self.grid[i]
            for j in range(1, self.width - 1):
                row[j] = MagicValues.OPEN.value

        for (dx, dy) in P42:
            x = center_x + dx
            y = center_y + dy
            if (x < 0 or x >= self.width or y < 0 or y >= self.height):
                print("Warning: Maze too small for 42 pattern!")
                return False
            self.grid[y][x] = MagicValues.PATTERN.value
            self.blocked.add((x, y))
        return True

    def _carve_maze(self) -> None: ...
