

from pydantic import BaseModel, Field, ValidationError, modelValidator
from typing import Self
import sys


class Config(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry_x: int = Field(ge=0)
    entry_y: int = Field(ge=0)
    exit_x: int = Field(ge=0)
    exit_y: int = Field(ge=0)
    output_file: str = Field(min_length=0)
    perfect: bool

    @modelValidator(mode="after")
    def validation_regulament(self) -> Self:
        return self


def open_file() -> tuple[bool, str]:
    if len(sys.argv) != 2:
        print("There should be only two arguments.")
        return
    try:
        with open(sys.argv[1]) as file:
            return (True, file.read())
    except (FileNotFoundError, FileExistsError) as e:
        print(f"Error Opening File: {e}")
        return(False, str(e))


def parsing(file: str) -> dict:
    lines = file.splitlines()
    data = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        else:
            try:
                key, _, value = line.partition("=")
                data[key.strip()] = value.strip()
            except ValidationError as e:
                print("Expected validation error:\n")
                for error in e.errors():
                    print(error["msg"])


def main() -> None:
    pass


if __name__ == "__main__":
    main()
