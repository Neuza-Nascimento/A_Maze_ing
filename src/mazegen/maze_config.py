import secrets
from typing import Self

from pydantic import BaseModel, Field, model_validator


class MazeConfig(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: tuple[int, int] = Field(min_length=2, max_length=2)
    exit: tuple[int, int] = Field(min_length=2, max_length=2)
    output_file: str = Field(default="maze.txt")
    perfect: bool
    seed: int | None = Field(default=secrets.randbits(32))
    algorithm: str | None = Field(default="DFS")
    display: str | None = Field(default="MLX")

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
        return self
