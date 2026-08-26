import random
from pathlib import Path
from typing import TYPE_CHECKING

from .magic_values import (
    DIMENSIONS,
    DIR_LETTER,
    DIRECTIONS,
    MIN_8,
    OPPOSITE,
    MagicValues,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from mazegen import MazeConfig
from collections import deque


class MazeGenerator:
    """Generate, solve, and expose a configurable maze.

    The generator supports multiple maze-generation algorithms and can
    produce either perfect or imperfect mazes according to the configuration.
    """

    def __init__(self, config: MazeConfig) -> None:
        """Initialize a maze generator from the supplied configuration.

        Args:
            config: Configuration containing maze dimensions, entry and exit,
                generation options, and output settings.
        """
        self.config: MazeConfig = config
        self._width: int = config.width
        self._height: int = config.height
        self._grid: list[list[int]] = []
        self._blocked: set[tuple[int, int]] = set()
        random.seed(config.seed)
        self._create_grid()
        self._solution: list[str] = []

    def _create_grid(self) -> None:
        """Create the initial closed grid and apply the 42 pattern.

        The outer border is marked as blocked before the 42 pattern is
        inserted into the grid.
        """
        n: int = MagicValues.CLOSED.value
        for _ in range(self._height):
            row: list[int] = [n for _ in range(self._width)]
            self._grid.append(row)
        self._42_pattern()

    def _centered_origin(self, pattern: list[tuple[int, int]]) -> tuple[int, int]:
        """Calculate the origin needed to center a pattern in the maze.

        Args:
            pattern: Relative coordinates describing the pattern.

        Returns:
            The x and y coordinates of the pattern origin.
        """
        xs: list[int] = [dx for dx, _ in pattern]
        ys: list[int] = [dy for _, dy in pattern]

        pattern_width: int = max(xs) - min(xs) + 1
        pattern_height: int = max(ys) - min(ys) + 1

        center_x: int = (self._width - pattern_width) // 2 - min(xs)
        center_y: int = (self._height - pattern_height) // 2 - min(ys)

        return center_x, center_y

    def _42_pattern(self) -> None:
        """Place the 42 pattern at the center when the maze is large enough.

        A warning is printed when the maze dimensions are too small for the
        required pattern.
        """

        def draw(pattern: list[tuple[int, int]]) -> None:
            """Draw one 42-pattern component on the maze grid.

            Args:
                pattern: Relative coordinates describing the component.
            """
            center_x, center_y = self._centered_origin(pattern)
            for dx, dy in pattern:
                x, y = center_x + dx, center_y + dy
                if not (0 <= x < self._width and 0 <= y < self._height):
                    print("Warning: Maze too small for 42 pattern!")
                    return
                self._grid[y][x] = MagicValues.CLOSED.value
                self._blocked.add((x, y))

        for lo, hi, pattern in DIMENSIONS:
            if lo <= self._height <= hi or lo <= self._width <= hi:
                draw(pattern)
            if (MIN_8 - 1) in {self._width, self._height}:
                print("Warning, maze too small for the 42 Pattern!")

    def _dfs(self) -> None:
        """Generate a maze using depth-first search backtracking.

        The algorithm starts at the configured entry and opens walls while
        visiting unvisited neighbouring cells.
        """
        visited: set[tuple[int, int]] = {self.config.entry}
        stack: list[tuple[int, int]] = [self.config.entry]
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
        """Generate a maze using Kruskal's minimum spanning tree algorithm.

        Candidate walls are shuffled and removed when doing so joins two
        previously disconnected cell sets.
        """
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
            """Find the representative of a cell's disjoint-set group.

            Args:
                cell: Cell whose set representative is requested.

            Returns:
                The representative cell of the set.
            """
            if daddy[cell] != cell:
                daddy[cell] = find(daddy[cell])
            return daddy[cell]

        def union(cell1: tuple[int, int], cell2: tuple[int, int]) -> bool:
            """Join two disjoint cell sets when they are different.

            Args:
                cell1: First cell to join.
                cell2: Second cell to join.

            Returns:
                True when the two sets were joined, otherwise False.
            """
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

    def _prim(self) -> None:
        """Generate a maze using randomized Prim's algorithm.

        The algorithm grows the maze from the configured entry by selecting
        random walls from the current frontier.
        """
        in_maze: set[tuple[int, int]] = {self.config.entry}
        frontier: list[tuple[tuple[int, int], MagicValues, tuple[int, int]]] = []

        def get_walls(cell: tuple[int, int]) -> None:
            """Add eligible neighbouring walls to the frontier.

            Args:
                cell: Cell whose neighbouring walls should be considered.
            """
            for direction, (dx, dy) in DIRECTIONS.items():
                nx, ny = cell[0] + dx, cell[1] + dy
                if (nx, ny) in self._blocked or (nx, ny) in in_maze:
                    continue
                if not (0 <= nx < self._width and 0 <= ny < self._height):
                    continue
                frontier.append((cell, direction, (nx, ny)))

        get_walls(self.config.entry)

        while frontier:
            i: int = random.randrange(len(frontier))
            (cx, cy), direction, neighbour = frontier.pop(i)
            if neighbour in in_maze:
                continue

            nx, ny = neighbour
            self._grid[cy][cx] &= ~direction.value
            self._grid[ny][nx] &= ~OPPOSITE[direction.value]
            in_maze.add(neighbour)
            get_walls(neighbour)

    def _bfs(self) -> list[str]:
        """Find the shortest path from the entry to the exit using BFS.

        Returns:
            A list of direction letters representing the shortest path, or
            an empty list when the exit cannot be reached.
        """
        queque: deque[tuple[tuple[int, int], list[str]]] = deque([(self.config.entry, [])])

        walls_visited: set[tuple[int, int]] = {self.config.entry}

        while queque:
            position, path = queque.popleft()
            px, py = position

            if position == self.config.exit:
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

    def _imperfect(self) -> None:
        """Open selected walls to create routes in a non-perfect maze.

        Walls adjacent to cells with only one open side are prioritized in
        order to reduce dead ends while preserving maze connectivity.
        """

        def open_count(cell: tuple[int, int]) -> int:
            """Count the open passages connected to a cell.

            Args:
                cell: Cell whose open neighbouring passages are counted.

            Returns:
                The number of open passages from the cell.
            """
            px, py = cell
            count = 0
            for direction, (dx, dy) in DIRECTIONS.items():
                nx = dx + px
                ny = dy + py
                if nx < 0 or nx >= self._width:
                    continue
                if ny < 0 or ny >= self._height:
                    continue
                if (nx, ny) in self._blocked:
                    continue
                if not (self._grid[py][px] & direction.value):
                    count += 1
            return count

        walls: list[tuple[tuple[int, int], tuple[int, int], MagicValues]] = []
        priority_walls: list[tuple[tuple[int, int], tuple[int, int], MagicValues]] = []

        for y in range(self._height):
            for x in range(self._width):
                if (x, y) in self._blocked:
                    continue
                for direction, (_dx, _dy), otherdir in (
                    (MagicValues.EAST, (1, 0), (x + 1, y)),
                    (MagicValues.SOUTH, (0, 1), (x, y + 1)),
                ):
                    nx, ny = otherdir
                    if not (0 <= nx < self._width and 0 <= ny < self._height):
                        continue
                    if (nx, ny) in self._blocked:
                        continue
                    if not (self._grid[y][x] & direction.value):
                        continue

                    wall = (x, y), otherdir, direction
                    if open_count((x, y)) == 1 or open_count((nx, ny)) == 1:
                        priority_walls.append(wall)
                    else:
                        walls.append(wall)

        if not priority_walls:
            return

        random.shuffle(priority_walls)
        for wall in priority_walls:
            cell1, cell2, direct = wall
            if open_count(cell1) == 1 or open_count(cell2) == 1:
                self._grid[cell1[1]][cell1[0]] &= ~direct.value
                self._grid[cell2[1]][cell2[0]] &= ~OPPOSITE[direct.value]

        return

    def _output_res(self, path: list[str]) -> None:
        """Write the generated maze, coordinates, and solution to a file.

        Args:
            path: Direction letters forming the shortest path from entry to
                exit.
        """
        output = Path(self.config.output_file)
        with output.open(mode="w", encoding="utf-8") as f:
            for row in self._grid:
                for num in row:
                    f.write(hex(num)[-1].upper())
                f.write("\n")
            f.write("\n")
            f.write(f"{self.config.entry[0]}, {self.config.entry[1]}\n")
            f.write(f"{self.config.exit[0]}, {self.config.exit[1]}\n")
            f.write("\n")
            for s in path:
                f.write(f"{s}")
            f.write("\n")

    def generate(self) -> None:
        """Generate the maze using the configured algorithm.

        The selected algorithm is executed first. If the maze is configured
        as non-perfect, additional walls are opened to create loops and
        reduce dead ends.
        """
        name: str | None = self.config.algorithm
        algos: dict[str, Callable[[], None]] = {
            "DFS": self._dfs,
            "KRUSKAL": self._kruskal,
            "PRIM": self._prim,
        }
        for algo, func in algos.items():
            if algo == name:
                func()
                break
            self._kruskal()
            break

        if not self.config.perfect:
            self._imperfect()

    def solve(self) -> bool:
        """Solve the generated maze and write the solution to the output file.

        Returns:
            True when a path from entry to exit is found, otherwise False.
        """
        path: list[str] = self._bfs()
        if not path:
            print("Unable to find a solution!\n")
            return False
        self._solution = path
        self._output_res(path)
        return True

    def get_solution(self) -> list[str]:
        """Return the most recently computed solution path.

        Returns:
            The solution as a list of direction letters.
        """
        return self._solution

    def get_grid(self) -> list[list[int]]:
        """Return the current internal maze grid.

        Returns:
            The maze grid represented as hexadecimal wall values.
        """
        return self._grid

    def get_height(self) -> int:
        """Return the height attribute

        Returns:
            The maze height
        """
        return self._height

    def get_width(self) -> int:
        """Return the width attribute

        Returns:
            The maze width
        """
        return self._width
