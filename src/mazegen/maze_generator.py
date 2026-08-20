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
        self._config: MazeConfig = config
        self._width: int = config.width
        self._height: int = config.height
        self._grid: list[list[int]] = []
        self._blocked: set[tuple[int, int]] = set()
        random.seed(config.seed)
        self._create_grid()

    def _create_grid(self) -> None:
        n: int = MagicValues.CLOSED.value
        for y in range(self._height):
            row: list[int] = []
            for x in range(self._width):
                if y in {0, self._height - 1} or x in {0, self._width - 1}:
                    self._blocked.add((x, y))
                row.append(n)
            self._grid.append(row)
        self._42_pattern()

    def _centered_origin(
        self, pattern: list[tuple[int, int]]
    ) -> tuple[int, int]:
        xs: list[int] = [dx for dx, _ in pattern]
        ys: list[int] = [dy for _, dy in pattern]

        pattern_width: int = max(xs) - min(xs) + 1
        pattern_height: int = max(ys) - min(ys) + 1

        center_x: int = (self._width - pattern_width) // 2 - min(xs)
        center_y: int = (self._height - pattern_height) // 2 - min(ys)

        return center_x, center_y

    def _42_pattern(self) -> bool:
        def draw(pattern: list[tuple[int, int]]) -> bool:
            center_x, center_y = self._centered_origin(pattern)
            for dx, dy in pattern:
                x, y = center_x + dx, center_y + dy
                if not (0 <= x < self._width and 0 <= y < self._height):
                    print("Warning: Maze too small for 42 pattern!")
                    return False
                self._grid[y][x] = MagicValues.CLOSED.value
                self._blocked.add((x, y))
            return True

        size_patterns: list[tuple[int, int, list[tuple[int, int]]]] = [
            (MIN_8, MAX_8, P42_8),
            (MIN_16, MAX_16, P42_16),
            (MIN_32, MAX_32, P42_32),
        ]

        for lo, hi, pattern in size_patterns:
            if lo <= self._height <= hi or lo <= self._width <= hi:
                return draw(pattern)
            if (MIN_8 - 1) in {self._width, self._height}:
                print("Warning, maze too small for the 42 Pattern!")
                return False
        return True

    def _dfs(self) -> None:
        visited: set[tuple[int, int]] = {self._config.entry}
        stack: list[tuple[int, int]] = [self._config.entry]
        while stack:
            cx, cy = stack[-1]
            neighbors: list[tuple[MagicValues, int, int]] = []
            for k, (dx, dy) in DIRECTIONS.items():
                nx, ny = cx + dx, cy + dy
                if (nx, ny) in self._blocked or (nx, ny) in visited:
                    continue
                if not (0 <= nx < self._width and 0 <= ny < self._height):
                    continue
                neighbors.append((k, nx, ny))

            if not neighbors:
                stack.pop()
                continue

            key, nnx, nny = random.choice(neighbors)
            self._grid[cy][cx] &= ~key.value
            self._grid[nny][nnx] &= ~OPPOSITE[key.value]
            stack.append((nnx, nny))
            visited.add((nnx, nny))

    def _kruskal(self) -> None:
        daddy: dict[tuple[int, int], tuple[int, int]] = {}
        walls: list[tuple[tuple[int, int], tuple[int, int], MagicValues]] = []

        for y in range(self._height):
            for x in range(self._width):
                if (x, y) in self._blocked:
                    continue
                daddy[x, y] = x, y
                if self._width > (x + 1) and (x + 1, y) not in self._blocked:
                    walls.append(((x, y), (x + 1, y), MagicValues.EAST))

                if self._height > (y + 1) and (x, y + 1) not in self._blocked:
                    walls.append(((x, y), (x, y + 1), MagicValues.SOUTH))

        def find(cell: tuple[int, int]) -> tuple[int, int]:
            if daddy[cell] != cell:
                daddy[cell] = find(daddy[cell])
            return daddy[cell]

        def union(cell1: tuple[int, int], cell2: tuple[int, int]) -> bool:
            source1: tuple[int, int] = find(cell1)
            source2: tuple[int, int] = find(cell2)

            if source1 != source2:
                daddy[source1] = source2
                return True
            return False

        random.shuffle(walls)
        for wall in walls:
            cell1, cell2, direct = wall
            if union(cell1, cell2):
                self._grid[cell1[1]][cell1[0]] &= ~direct.value
                self._grid[cell2[1]][cell2[0]] &= ~OPPOSITE[direct.value]

    def _prim(self) -> list[str]:
        return []

    def _bfs(self) -> list[str]:
        queque: deque[tuple[tuple[int, int], list[str]]] = deque(
            [(self._config.entry, [])]
        )

        walls_visited: set[tuple[int, int]] = {self._config.entry}

        while queque:
            position, path = queque.popleft()
            px, py = position

            if position == self._config.exit:
                return path

            for direction, (dx, dy) in DIRECTIONS.items():
                nx = dx + px
                ny = dy + py

                if nx < 0 or nx >= self._width:
                    continue

                if ny < 0 or ny >= self._height:
                    continue

                if (nx, ny) in walls_visited:
                    continue

                if self._grid[py][px] & direction.value:
                    continue

                walls_visited.add((nx, ny))
                queque.append(((nx, ny), [*path, DIR_LETTER[direction]]))

        return []

    def _output_res(self, path: list[str]) -> None:
        output = Path(self._config.output_file)
        with output.open(mode="w", encoding="utf-8") as f:
            for row in self._grid[1:-1]:
                for num in row[1:-1]:
                    f.write(hex(num)[-1].upper())
                f.write("\n")
            f.write("\n")
            f.write(f"{self._config.entry[0]}, {self._config.entry[1]}\n")
            f.write(f"{self._config.exit[0]}, {self._config.exit[1]}\n")
            f.write("\n")
            for s in path:
                f.write(f"{s}")
            f.write("\n")

    def generate(self) -> bool:
        solved_path: list[str]
        if self._config.perfect:
            self._kruskal()
            solved_path = self._bfs()
        else:
            self._dfs()
            solved_path = self._bfs()
        if not solved_path:
            print("Unable to find a solution!\n")
            return False
        self._output_res(solved_path)
        return True

    def get_grid(self) -> list[list[int]]:
        return self._grid
