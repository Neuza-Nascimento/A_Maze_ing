import secrets
from typing import Self

from pydantic import BaseModel, Field, model_validator

from .magic_values import DIMENSIONS, MIN_8


class MazeConfig(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = Field(default_factory=lambda: secrets.randbits(32))
    algorithm: str | None = Field(default="dfs")
    display: str | None = Field(default="mlx")

    @model_validator(mode="after")
    def validate_config(self) -> Self:
        if self.entry == self.exit:
            equal_points: str = "EXIT and ENTRY must not have equal points!"
            raise ValueError(equal_points)
        sx, sy = self.entry
        if sx <= 0 or sx >= self.width - 1 or sy <= 0 or sy >= self.height - 1:
            enrr: str = f"Entry (X={sx},Y={sy}) out of bounds!"
            raise ValueError(enrr)
        ex, ey = self.exit
        if ex <= 0 or ex >= self.width - 1 or ey <= 0 or ey >= self.height - 1:
            exrr: str = f"Exit (X={ex},Y={ey}) out of bounds!"
            raise ValueError(exrr)

        for lo, hi, pattern in DIMENSIONS:
            if (MIN_8 - 1) in {self.width, self.height}:
                return self
            if lo <= self.height <= hi or lo <= self.width <= hi:
                check: bool = self.__something(pattern)
                if not check:
                    in_pattern: str = "ENTRY or EXIT inside Pattern 42"
                    raise ValueError(in_pattern)
        return self

    def __something(self, pattern: list[tuple[int, int]]) -> bool:
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
