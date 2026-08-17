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
