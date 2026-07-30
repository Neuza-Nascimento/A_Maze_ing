from enum import IntFlag


class Wall(IntFlag):
    NORTH = 1  # bit 0 (LSB)
    EAST = 2   # bit 1
    SOUTH = 4  # bit 2
    WEST = 8   # bit 3


OPPOSITE: dict[Wall, Wall] = {
    Wall.NORTH: Wall.SOUTH,
    Wall.SOUTH: Wall.NORTH,
    Wall.WEST: Wall.EAST,
    Wall.EAST: Wall.WEST
}


DELTA: dict[Wall, tuple[int, int]] = {
    Wall.NORTH: (0, -1),
    Wall.SOUTH: (0, 1),
    Wall.WEST: (-1, 0),
    Wall.EAST: (1, 0),
}
