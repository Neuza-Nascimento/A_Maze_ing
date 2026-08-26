"""Maze Configuration.

The maze_configuration module grants access to the MazeConfig class,
that is later used by the MazeGenerator class as its only parameter.

It requires that a width, height, entry, exit, output_file and perfect
are passed to it, being only the seed and algorithm optional to it.
"""

import secrets
from typing import Self

from pydantic import BaseModel, Field, model_validator

from .magic_values import DIMENSIONS, MIN_8


class MazeConfig(BaseModel):
    """Maze Configuration Model.

    Holds all the key=value pairs found in the config file.
    """

    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = Field(default_factory=lambda: secrets.randbits(32))
    algorithm: str | None = Field(default="dfs")

    @model_validator(mode="after")
    def validate_config(self) -> Self:
        """Validate Configuration.

        Whether the configuration for ENTRY or EXIT are between
        the specified width and height range.

        Returns:
            Self: PYDANTIC REQUIRES FUNCTIONS WITH THE MODEL_VALIDATOR DECORATOR
                TO RETURN SELF

        Raises:
            ValueError: Entry and Exit are the same coordinates
            ValueError: Entry is higher than (self.width - 1) or (self.height - 1)
            ValueError: Exit is higher than (self.width - 1) or (self.height - 1)
            ValueError: Entry or Exit coordinates are placed inside the 42 Pattern

        """
        if self.entry == self.exit:
            equal_points: str = "EXIT and ENTRY must not have equal points!"
            raise ValueError(equal_points)
        sx, sy = self.entry
        if sx >= self.width - 1 or sy >= self.height - 1:
            enrr: str = f"Entry (X={sx},Y={sy}) out of bounds!"
            raise ValueError(enrr)
        ex, ey = self.exit
        if ex >= self.width - 1 or ey >= self.height - 1:
            exrr: str = f"Exit (X={ex},Y={ey}) out of bounds!"
            raise ValueError(exrr)

        for lo, hi, pattern in DIMENSIONS:
            if (MIN_8 - 1) in {self.width, self.height}:
                return self
            if lo <= self.height <= hi or lo <= self.width <= hi:
                check: bool = self.__check_pattern(pattern)
                if not check:
                    in_pattern: str = "ENTRY or EXIT inside Pattern 42"
                    raise ValueError(in_pattern)
        return self

    def __check_pattern(self, pattern: list[tuple[int, int]]) -> bool:
        """Check whether the Entry or Exit are placed inside the 42 pattern.

        Args:
            pattern (list[tuple[int, int]]): The 42 pattern to be used

        Returns:
            bool: True if entry or exit points are not inside the 42 pattern
                False otherwise

        """
        xs: list[int] = [dx for dx, _ in pattern]
        ys: list[int] = [dy for _, dy in pattern]

        pattern_width: int = max(xs) - min(xs) + 1
        pattern_height: int = max(ys) - min(ys) + 1

        center_x: int = (self.width - pattern_width) // 2 - min(xs)
        center_y: int = (self.height - pattern_height) // 2 - min(ys)

        for dx, dy in pattern:
            x, y = center_x + dx, center_y + dy
            if (x, y) in {self.entry, self.exit}:
                return False
        return True
