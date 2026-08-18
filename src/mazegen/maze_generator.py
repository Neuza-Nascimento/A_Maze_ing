import random
from pathlib import Path
from typing import TYPE_CHECKING

from .magic_values import (
    DIR_LETTER,
    DIRECTIONS,
    MAX_8,
    MAX_16,
    MAX_32,
    MIN_8,
    MIN_16,
    MIN_32,
    OPPOSITE,
    P42_8,
    P42_16,
    P42_32,
    MagicValues,
)

if TYPE_CHECKING:
    from mazegen import MazeConfig
from collections import deque


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

    def _centered_origin(
        self, pattern: list[tuple[int, int]]
    ) -> tuple[int, int]:
        xs: list[int] = [dx for dx, _ in pattern]
        ys: list[int] = [dy for _, dy in pattern]

        pattern_width: int = max(xs) - min(xs) + 1
        pattern_height: int = max(ys) - min(ys) + 1

        center_x: int = (self.width - pattern_width) // 2 - min(xs)
        center_y: int = (self.height - pattern_height) // 2 - min(ys)

        return center_x, center_y

    def _42_pattern(self) -> bool:
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

        size_patterns: list[tuple[int, int, list[tuple[int, int]]]] = [
            (MIN_8, MAX_8, P42_8),
            (MIN_16, MAX_16, P42_16),
            (MIN_32, MAX_32, P42_32),
        ]

        for lo, hi, pattern in size_patterns:
            if lo <= self.height <= hi or lo <= self.width <= hi:
                return draw(pattern)
            if (MIN_8 - 1) in {self.width, self.height}:
                print("Warning, maze too small for the 42 Pattern!")
                return False
        return True

    def _imperfect_dfs(self) -> set[tuple[int, int]]:
        visited: set[tuple[int, int]] = {self.config.entry}
        stack: list[tuple[int, int]] = [self.config.entry]
        while stack:
            cx, cy = stack[-1]
            neighbors: list = []
            for k, (dx, dy) in DIRECTIONS.items():
                nx, ny = cx + dx, cy + dy
                if (nx, ny) in self.blocked or (nx, ny) in visited:
                    continue
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                neighbors.append((k, nx, ny))

            if not neighbors:
                stack.pop()
                continue

            key, nnx, nny = random.choice(neighbors)
            self.grid[cy][cx] &= ~key.value
            self.grid[nny][nnx] &= ~OPPOSITE[key.value]
            stack.append((nnx, nny))
            visited.add((nnx, nny))
        return visited

    def _perfect_dfs(self) -> None:
        visited_walls = self._imperfect_dfs()

    def _bfs(self) -> list[str]:
        queque: deque[tuple[tuple[int, int], list[str]]] = deque(
            [(self.config.entry, [])]
        )

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

                if self.grid[py][px] & direction.value:
                    continue

                walls_visited.add((nx, ny))
                queque.append(((nx, ny), [*path, DIR_LETTER[direction]]))

        return []

    def output_res(self, path: list[str]) -> None:
        output = Path(self.config.output_file)
        with output.open(mode="w", encoding="utf-8") as f:
            for row in self.grid[1:-1]:
                for num in row[1:-1]:
                    f.write(hex(num)[-1].upper())
                f.write("\n")
            f.write("\n")
            f.write(f"{self.config.entry[0]}, {self.config.entry[1]}\n")
            f.write(f"{self.config.exit[0]}, {self.config.exit[1]}\n")
            f.write("\n")
            for s in path:
                f.write(f"{s}")
            f.write("\n")

    def generate(self) -> bool:
        if self.config.perfect:
            self._perfect_dfs()
            return True
        self._imperfect_dfs()
        solved_path: list[str] = self._bfs()
        if not solved_path:
            print("Unable to find a solution!\n")
            return False
        self.output_res(solved_path)
        return True
