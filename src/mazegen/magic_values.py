from enum import Enum


class MagicValues(Enum):
    OPEN = 0b0000
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000
    CLOSED = 0b1111


DIRECTIONS: dict[MagicValues, tuple[int, int]] = {
    MagicValues.NORTH: (0, -1),
    MagicValues.EAST: (1, 0),
    MagicValues.SOUTH: (0, 1),
    MagicValues.WEST: (-1, 0)
}


DIR_LETTER: dict[MagicValues, str] = {
    MagicValues.NORTH: "N",
    MagicValues.EAST:  "E",
    MagicValues.SOUTH: "S",
    MagicValues.WEST:  "W"
}

OPPOSITE: dict[int, int] = {
    MagicValues.NORTH.value: MagicValues.SOUTH.value,
    MagicValues.SOUTH.value: MagicValues.NORTH.value,
    MagicValues.EAST.value: MagicValues.WEST.value,
    MagicValues.WEST.value: MagicValues.EAST.value
}

MAX_32: int = 52
MIN_32: int = 18
P42_32: list[tuple[int, int]] = [
    (0, 0), (3, 0), (5, 0), (6, 0), (7, 0), (8, 0),
    (0, 1), (3, 1), (8, 1),
    (0, 2), (3, 2), (8, 2),
    (0, 3), (1, 3), (2, 3), (3, 3), (5, 3), (6, 3), (7, 3), (8, 3),
    (3, 4), (5, 4),
    (3, 5), (5, 5),
    (3, 6), (5, 6), (6, 6), (7, 6), (8, 6),
]

MAX_16: int = 17
MIN_16: int = 13
P42_16: list[tuple[int, int]] = [
    (0, 0), (2, 0), (4, 0), (5, 0), (6, 0),
    (0, 1), (2, 1), (6, 1),
    (0, 2), (1, 2), (2, 2), (4, 2), (5, 2), (6, 2),
    (2, 3), (4, 3),
    (2, 4), (4, 4), (5, 4), (6, 4)
]

MAX_8: int = 12
MIN_8: int = 10
P42_8: list[tuple[int, int]] = [
    (0, 1), (2, 1), (3, 1),
    (0, 2), (1, 2), (3, 2),
    (0, 3), (1, 3), (2, 3),
    (1, 4), (2, 4), (3, 4),
]

DIMENSIONS: list[tuple[int, int, list[tuple[int, int]]]] = [
    (MIN_8, MAX_8, P42_8),
    (MIN_16, MAX_16, P42_16),
    (MIN_32, MAX_32, P42_32),
]
