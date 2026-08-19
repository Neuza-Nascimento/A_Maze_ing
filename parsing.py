from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

import dotenv

from mazegen import MazeConfig, magic_values


def check_width(width: str) -> int:
    try:
        w = int(width)
    except ValueError as e:
        err = f"WIDTH must be an integer, got: {width}"
        raise ValueError(err) from e
    if w <= 0:
        zero: str = "WIDTH must be greater than 0"
        raise ValueError(zero)
    return w


def check_height(height: str) -> int:
    try:
        h = int(height)
    except ValueError as e:
        err = f"HEIGHT must be an integer, got: {height}"
        raise ValueError(err) from e
    if h <= 0:
        zero: str = "HEIGHT must be greater than 0"
        raise ValueError(zero)
    return h


def check_entry(entry_point: str) -> tuple[int, int]:
    err: str
    if "," not in entry_point:
        err = "Entry must be in format x,y"
        raise ValueError(err)
    x, y = entry_point.split(",")
    try:
        entry: tuple[int, int] = (int(x), int(y))
    except ValueError as e:
        err = f"ENTRY must be an integer, got: {entry_point}"
        raise ValueError(err) from e
    if entry[0] <= 0 or entry[1] <= 0:
        out_of_bounds: str = f"Entry ({x},{y}) out of bounds"
        raise ValueError(out_of_bounds)
    return entry


def check_exit(exit_point: str) -> tuple[int, int]:
    err: str
    if "," not in exit_point:
        err = "EXIT must be in format x,y"
        raise ValueError(err)
    x, y = exit_point.split(",")
    try:
        out: tuple[int, int] = (int(x), int(y))
    except ValueError as e:
        err = f"EXIT must be an integer, got: {exit_point}"
        raise ValueError(err) from e
    if out[0] <= 0 or out[1] <= 0:
        out_of_bounds: str = f"EXIT ({x},{y}) out of bounds"
        raise ValueError(out_of_bounds)
    return out


def check_file(file: str) -> str:
    if Path(file).exists():
        return file
    return file


def check_perfect(perfect: str) -> bool:
    if perfect in {"True", "TRUE"}:
        return True
    if perfect in {"False", "FALSE"}:
        return False
    staterr: str = f"PERFECT must be True or False, got: {perfect}"
    raise ValueError(staterr)


def check_seed(seed: str) -> int:
    try:
        sed = int(seed)
    except ValueError as e:
        err: str = f"SEED must be an integer, got: {seed}"
        raise ValueError(err) from e
    if sed <= 0:
        zero: str = "SEED must be greater than 0"
        raise ValueError(zero)
    return sed


def check_algo(algo: str) -> str:
    if not algo:
        return "dfs"
    return algo


def check_display(display: str) -> str:
    if not display:
        return "mlx"
    return display


checker: dict[str, Callable[[str], Any]] = {
    "WIDTH": check_width,
    "HEIGHT": check_height,
    "ENTRY": check_entry,
    "EXIT": check_exit,
    "OUTPUT_FILE": check_file,
    "PERFECT": check_perfect,
    "SEED": check_seed,
    "ALGORITHM": check_algo,
    "DISPLAY": check_display,
}


def parser(filename: str) -> MazeConfig:
    file = Path(filename)
    if not file.exists():
        fnf: str = "File Not Found"
        raise FileNotFoundError(fnf)

    raw: dict[str, str] = {}

    contents = file.read_text(encoding="utf-8")
    for line in contents.split("\n"):
        if line.startswith(("#", "\n")):
            continue
        if not line.strip():
            continue
        if "=" not in line:
            serr: str = "Invalid Syntax"
            raise SyntaxError(serr)

        key, value = line.split("=", 1)
        key = key.strip().upper()
        value = value.strip()
        raw[key] = value
    for key in magic_values.KEYS:
        if key not in raw:
            missing: str = f"Missing: {key}"
            raise ValueError(missing)

    config: dict[str, Any] = {}
    for k, v in raw.items():
        try:
            f = checker[k]
            config[k.lower()] = f(v)
        except ValueError as e:
            raise ValueError(str(e)) from e
    return MazeConfig(**config)


def parsing(filename: str) -> MazeConfig:
    path: str | None = dotenv.find_dotenv(filename)
    raw: dict[str, str | None] = dotenv.dotenv_values(path)

    for key in magic_values.KEYS:
        if key not in raw:
            missing: str = f"Missing: {key}"
            raise ValueError(missing)
    config: dict[str, Any] = {}
    for k, v in raw.items():
        try:
            f = checker[k]
            config[k.lower()] = f(str(v))
        except ValueError as e:
            raise ValueError(str(e)) from e
    return MazeConfig(**config)
