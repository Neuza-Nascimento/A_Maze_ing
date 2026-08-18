import random
from typing import TYPE_CHECKING

from .magic_values import (
    MAX_8,
    MAX_16,
    MAX_32,
    MIN_8,
    MIN_16,
    MIN_32,
    P42_8,
    P42_16,
    P42_32,
    MagicValues,
)

if TYPE_CHECKING:
    from mazegen import MazeConfig


class MazeGenerator:
    def __init__(self, config: MazeConfig) -> None:
        self.config: MazeConfig = config
        self.width: int = config.width
        self.height: int = config.height
        self.grid: list[list[int]] = []
        self.blocked: set[tuple[int, int]] = set()
        random.seed(config.seed)
        self._create_grid()

    def _create_grid(self) -> None:
        n: int = MagicValues.CLOSED.value
        for _ in range(self.height):
            row: list[int] = [n for _ in range(self.width)]
            self.grid.append(row)
        self._42_pattern()

    def _centered_origin(self, pattern: list[tuple[int, int]]) -> tuple[int, int]:
        xs = [dx for dx, _ in pattern]
        ys = [dy for _, dy in pattern]

        pattern_width = max(xs) - min(xs) + 1
        pattern_height = max(ys) - min(ys) + 1

        center_x = (self.width - pattern_width) // 2 - min(xs)
        center_y = (self.height - pattern_height) // 2 - min(ys)

        return center_x, center_y

    def _42_pattern(self) -> bool:
        open_row = [MagicValues.OPEN.value] * (self.width - 2)
        for row in self.grid[1:self.height - 1]:
            row[1:self.width - 1] = open_row

        def draw(pattern: list[tuple[int, int]]) -> bool:
            center_x, center_y = self._centered_origin(pattern)
            for dx, dy in pattern:
                x, y = center_x + dx, center_y + dy
                if not (0 <= x < self.width and 0 <= y < self.height):
                    print("Warning: Maze too small for 42 pattern!")
                    return False
                self.grid[y][x] = MagicValues.PATTERN.value
                self.blocked.add((x, y))
            return True

        size_patterns = [
            (MIN_8, MAX_8, P42_8),
            (MIN_16, MAX_16, P42_16),
            (MIN_32, MAX_32, P42_32),
        ]

        for lo, hi, pattern in size_patterns:
            if lo <= self.height <= hi and lo <= self.width <= hi:
                return draw(pattern)

        return True

    def _carve_maze(self) -> None: ...
