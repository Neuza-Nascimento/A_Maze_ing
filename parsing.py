"""Parsing configuration values for the maze generator."""

from pathlib import Path

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:

    from collections.abc import Callable

from mazegen import MazeConfig

KEYS: list[str] = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
]


def check_width(width: str) -> int:
    """Validate that the width is a positive integer.

    Args:
        width: Width value read from the configuration file.

    Returns:
        The validated width as an integer.
    """
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
    """Validate that the height is a positive integer.

    Args:
        height: Height value read from the configuration file.

    Returns:
        The validated height as an integer.
    """
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
    """Validate and parse the maze entry coordinates.

    Args:
        entry_point: Entry coordinates in x,y format.

    Returns:
        The entry coordinates as an integer tuple.
    """
    err: str

    if "," not in entry_point:
        err = "ENTRY must be in format x,y"
        raise ValueError(err)

    x, y = entry_point.split(",")

    try:
        entry: tuple[int, int] = (int(x), int(y))
    except ValueError as e:
        entryerr = f"ENTRY must be an integer, got: {entry_point}"
        raise ValueError(entryerr) from e

    return entry


def check_exit(exit_point: str) -> tuple[int, int]:
    """Validate and parse the maze exit coordinates.

    Args:
        exit_point: Exit coordinates in x,y format.

    Returns:
        The exit coordinates as an integer tuple.
    """
    err: str

    if "," not in exit_point:
        err = "EXIT must be in format x,y"
        raise ValueError(err)

    x, y = exit_point.split(",")

    try:
        out: tuple[int, int] = (int(x), int(y))
    except ValueError as e:
        exiterr = f"EXIT must be an integer, got: {exit_point}"
        raise ValueError(exiterr) from e

    return out


def check_file(file: str) -> str:
    """Validate that the output path is suitable for a file.

    Args:
        file: Name or path of the output file.

    Returns:
        The validated output filename.
    """
    path = Path(file)

    if path.is_dir():
        isdir: str = (
            f"OUTPUT_FILE must be a file, not a directory: {file}"
        )
        raise ValueError(isdir)

    parent = path.parent

    if not parent.exists():
        noparent: str = (
            f"OUTPUT_FILE directory does not exist: {parent}"
        )
        raise ValueError(noparent)

    return file


def check_perfect(perfect: str) -> bool:
    """Validate and convert the PERFECT configuration option.

    Args:
        perfect: PERFECT value read from the configuration file.

    Returns:
        True or False according to the configuration value.
    """
    if perfect in {"True", "TRUE"}:
        return True

    if perfect in {"False", "FALSE"}:
        return False

    staterr: str = f"PERFECT must be True or False, got: {perfect}"
    raise ValueError(staterr)


def check_seed(seed: str) -> int:
    """Validate that the seed is a positive integer.

    Args:
        seed: Seed value read from the configuration file.

    Returns:
        The validated seed as an integer.
    """
    try:
        sed = int(seed)
    except ValueError as e:
        seederr: str = f"SEED must be an integer, got: {seed}"
        raise ValueError(seederr) from e

    if sed <= 0:
        zero: str = "SEED must be greater than 0"
        raise ValueError(zero)

    return sed


def check_algo(algo: str) -> str:
    """Validate the selected maze generation algorithm.

    Args:
        algo: Algorithm name read from the configuration file.

    Returns:
        The validated algorithm name.
    """
    for c in algo:
        if c.isspace() or c.isnumeric() or c.isdecimal() or c in {"-", "+"}:
            algo_err: str = f"Invalid ALGORITHM, got: {algo}"
            raise ValueError(algo_err)

    if algo in {"dfs", "kruskal", "prim"}:
        return algo

    msg: str = f"ALGORITHM option not supported ({algo})"
    raise ValueError(msg)


def check_display(display: str) -> str:
    """Validate the selected maze display mode.

    Args:
        display: Display mode read from the configuration file.

    Returns:
        The validated display mode.
    """
    for c in display:
        if c.isspace() or c.isnumeric() or c.isdecimal() or c in {"-", "+"}:
            display_error: str = f"Invalid DISPLAY, got: {display}"
            raise ValueError(display_error)

    if display == "mlx":
        return display

    msg: str = f"DISPLAY option not supported ({display})"
    raise ValueError(msg)


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
    """Parse a maze configuration file into a MazeConfig object.

    Args:
        filename: Path to the configuration file.

    Returns:
        A MazeConfig instance containing the validated configuration.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        SyntaxError: If a configuration line does not contain an equals sign.
        ValueError: If a required key is missing or a configuration value
            fails validation.
    """
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

    for key in KEYS:
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

