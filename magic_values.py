from enum import Enum


class MagicValues(Enum):
    OPEN = 0b0000
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000
    PATTERN = 0b1001
    POINT = 0b1010
    CENTER = 0b1110
    CLOSED = 0b1111


P42: list[tuple[int, int]] = [
    (0, 0), (3, 0), (5, 0), (6, 0), (7, 0), (8, 0),
    (0, 1), (3, 1), (8, 1),
    (0, 2), (3, 2), (8, 2),
    (0, 3), (1, 3), (2, 3), (3, 3), (5, 3), (6, 3), (7, 3), (8, 3),
    (3, 4), (5, 4),
    (3, 5), (5, 5),
    (3, 6), (5, 6), (6, 6), (7, 6), (8, 6),
]
