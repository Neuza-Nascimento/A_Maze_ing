from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Self


class MazeConfig(BaseModel):
    width: int = Field(gt=0, le=10000)
    height: int = Field(gt=0, le=10000)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(min_length=1)
    perfect: bool

    @model_validator(mode="after")
    def validate(self) -> Self:
        if not self.entry.x < self.width and self.entry.y < self.height:
            raise ValueError("")
        if not exit.exit.x < self.width and self.exit.y < self.height:
            raise ValueError("")
        if self.entry == self.exit:
            raise ValueError("")
        return self


def extract_data(file: str) -> tuple[bool, dict | str]:
    lines = file.splitlines()
    data = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        else:
            item = line.split("=")
            if len(item) != 2:
                raise ValueError("Missing arguments")
            data[item[0].strip()] = item[1].strip()
    return (True, data)


def split_xy(coord: str) -> tuple[int, int]:
    data = coord.split(",", maxsplit=1)
    if len(data) != 2:
        raise ValueError("Error")
    return int(data[0]), int(data[1])


def parsing(filestr: str) -> MazeConfig:
    keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    try:
        with open(filestr) as file:
            data = extract_data(file.read())
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error opening or reading file: {e}")
    except ValueError as e:
        raise ValueError(f"Variable not valid: {e}")
    for key in keys:
        if key not in data[1]:
            raise ValueError(f"Missing variable {key}")
    print(split_xy(data[1]["ENTRY"]))
    try:
        config = MazeConfig(
                width=data[1]["WIDTH"],
                height=data[1]["HEIGHT"],
                entry_x=split_xy(data[1]["ENTRY"]),
                entry_y=split_xy(data[1]["EXIT"]),
                output_file=data[1]["OUTPUT_FILE"],
                perfect=data[1]["PERFECT"],
        )
        return config
    except ValidationError as e:
        raise ValueError(e)
        # for error in e.errors():
        #     raise ValueError(error["msg"]) from e
