import secrets
from typing import Self

from pydantic import BaseModel, Field, model_validator


class MazeConfig(BaseModel):
    width: int = Field(gt=0, le=100)
    height: int = Field(gt=0, le=100)
    entry: tuple[int, int] = Field(min_length=2, max_length=2)
    exit: tuple[int, int] = Field(min_length=2, max_length=2)
    output_file: str = Field(default="maze.txt")
    perfect: bool
    seed: int | None = Field(default=secrets.randbits(32))
    algorithm: str | None = Field(default="bfs")
    display: str | None = Field(default="mlx")

    @model_validator(mode="after")
    def validate_config(self) -> Self:
        ex, ey = self.entry
        enerr: str = f"Exit (X={ex}, Y={ey}) must be smaller than"
        if ex > self.width:
            werr = f"{enerr} Width: (X={self.width})!"
            raise ValueError(werr)
        if ey > self.height:
            herr = f"{enerr} Height: (Y={self.height})!"
            raise ValueError(herr)
        sx, sy = self.exit
        exerr: str = f"Exit (X={sx}, Y={sy}) must be smaller than"
        if sx > self.width:
            werr = f"{exerr} Width: (X={self.width})!"
            raise ValueError(werr)
        if sy > self.height:
            herr = f"{exerr} Height: (Y={self.height})!"
            raise ValueError(herr)
        if ex == sx and ey == sy:
            ez: str = f"Entry({ex},{ey})"
            sz: str = f"Exit({sx},{sy})"
            same_points: str = f"{ez} and {sz} must be different values"
            raise ValueError(same_points)
        return self
