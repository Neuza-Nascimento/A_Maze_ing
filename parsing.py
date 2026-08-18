from typing import Self

from pydantic import BaseModel, Field, ValidationError, model_validator


class MazeConfig(BaseModel):
    width: int = Field(gt=0, le=10000)
    height: int = Field(gt=0, le=10000)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(min_length=1)
    perfect: bool

    @model_validator(mode="after")
    def validate_coordinates(self) -> Self:
        if not (self.entry[0] < self.width and self.entry[1] < self.height):
            raise ValueError(f"ENTRY {self.entry} is outside the maze bounds "
                             f"(width={self.width}, height={self.height})")
        if not (self.exit[0] < self.width and self.exit[1] < self.height):
            raise ValueError(f"EXIT {self.exit} is outside the maze bounds "
                             f"(width={self.width}, height={self.height})")
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT cannot have the same coordinates")
        return self


def extract_data(file: str) -> dict:
    lines = file.splitlines()
    data = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        else:
            item = line.split("=")
            if len(item) != 2:
                raise ValueError("Usage: key=value")
            data[item[0].strip()] = item[1].strip()
    return data


def split_xy(coord: str) -> tuple[int, int]:
    data = coord.split(",", maxsplit=1)
    if len(data) != 2:
        raise ValueError("Usage: key=value1,value2")
    return int(data[0]), int(data[1])


def parsing(filestr: str) -> MazeConfig:
    keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    try:
        with open(filestr) as file:
            data = extract_data(file.read())
    except FileNotFoundError as e:
        raise FileNotFoundError(e)
    except ValueError as e:
        raise ValueError(e)

    for key in keys:
        if key not in data:
            raise ValueError(f"Missing variable {key}")

    try:
        config = MazeConfig(
                width=data["WIDTH"],
                height=data["HEIGHT"],
                entry=split_xy(data["ENTRY"]),
                exit=split_xy(data["EXIT"]),
                output_file=data["OUTPUT_FILE"],
                perfect=data["PERFECT"],
        )
        return config
    except ValidationError as e:
        for error in e.errors():
            raise ValueError(error["msg"])
