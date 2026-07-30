from helpers import Wall


class Grid():
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        full = Wall.NORTH | Wall.EAST | Wall.SOUTH | Wall.WEST
        self.cells: list[list[Wall]] = [[full for _ in range(width)] for _ in range(height)]

