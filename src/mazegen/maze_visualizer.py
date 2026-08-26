"""Maze Visualizer."""

import random

from lib.mlx import Mlx

from .magic_values import DIR_BY_LETTER, Key, MagicValues
from .maze_generator import MazeGenerator


class MazeVisualizer:
    """Display visual representation of the generated maze by the mazeGenerator Class."""

    def __init__(self, generator: MazeGenerator) -> None:
        """Initilise MLX & the MazeVisualizer Class.

        Args:
            generator (MazeGenerator): MazeGenerator object that holds
                the grid, configurations and solved path

        """
        self.gen: MazeGenerator = generator
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.cell_size: int = 30
        self.maze_height: int = self.gen.get_height() * self.cell_size
        self.maze_width: int = self.gen.get_width() * self.cell_size
        self.window_height: int = self.maze_height + 100
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.maze_width, self.window_height, "A-maze-ing"
        )
        self.color_themes: list[dict[str, int]] = [self.generate_color_palette() for _ in range(5)]
        self.current_theme_index: int = 0
        self.current_colors: dict[str, int] = self.color_themes[self.current_theme_index].copy()
        self.border_size: int = 1
        self.path_cells: list[tuple[int, int]] = []
        self.path_step: int = 0
        self.is_animating: bool = False

    @staticmethod
    def random_color(r: tuple[int, int], g: tuple[int, int], b: tuple[int, int]) -> int:
        """Pick a random color from the given arguments.

        Args:
            r (tuple[int,int]): Min & Max range for the color red
            g (tuple[int,int]): Min & Max range for the color green
            b (tuple[int,int]): Min & Max range for the color blue

        Returns:
            int: a random color from the given ranges.

        """
        red = random.randint(r[0], r[1])
        green = random.randint(g[0], g[1])
        blue = random.randint(b[0], b[1])
        return (0xFF << 24) | (red << 16) | (green << 8) | blue

    def generate_color_palette(self) -> dict[str, int]:
        """Generate a color palette.

        Returns:
            dict[str, int]: Dictionary containing the color palette
                to be used by the visualizer

        """
        return {
            "WALL_COLOR": self.random_color((10, 509), (10, 50), (10, 50)),
            "PATH_COLOR": self.random_color((100, 200), (150, 255), (100, 200)),
            "ENTRY_COLOR": self.random_color((50, 150), (150, 255), (80, 180)),
            "EXIT_COLOR": self.random_color((200, 255), (50, 150), (50, 150)),
            "BORDER_COLOR": self.random_color((60, 120), (60, 120), (60, 120)),
            "CELL_COLOR": self.random_color((200, 255), (200, 255), (200, 255)),
            "TEXT_COLOR": self.random_color((10, 50), (10, 50), (10, 50)),
            "COLOR_15": self.random_color((200, 255), (180, 240), (50, 150)),
        }

    def apply_new_theme(self) -> None:
        """Apply the newly selected theme from the current color_themes list."""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.color_themes)
        self.current_colors = self.color_themes[self.current_theme_index].copy()

    def build_path_cells(self) -> list[tuple[int, int]]:
        """_summary_.

        Returns:
            list[tuple[int, int]]: path

        """
        path: list[tuple[int, int]] = []
        entry_x, entry_y = self.gen.config.entry
        row, col = entry_y, entry_x

        path.append((row, col))
        self.gen.solve()
        for letter in self.gen.get_solution():
            dr, dc = DIR_BY_LETTER[letter]
            row += dr
            col += dc
            path.append((row, col))
        return path

    def animate_path(self, _param: None) -> None:
        """Animate solved path.

        Args:
            _param (None): NECESSARY FOR MLX.

        """
        if not self.is_animating:
            return

        if self.path_step >= len(self.path_cells):
            self.is_animating = False
            return

        self.path_step += 1
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self._draw_maze(self.path_step)
        self.draw_menu()

    @staticmethod
    def _paint_rect(
        data: dict[slice[int, int, None], bytes],
        size_line: int,
        start: tuple[int, int],
        area: tuple[int, int],
        color: int,
    ) -> None:
        """Paint the pixels.

        Args:
            data (dict[slice[int, int, None], bytes]): imageptr
            size_line (int): how big the line should be
            start (tuple[int, int]): holds both x, y axis for the start
            area (tuple[int, int]): holds the width and height
            color (int): color to use

        """
        x_start, y_start = start
        width, height = area
        for y in range(height):
            for x in range(width):
                px = x_start + x
                py = y_start + y
                pos = py * size_line + px * 4
                data[pos : pos + 4] = color.to_bytes(4, "little")

    def _draw_maze(self, show_path_step: int = 0) -> None:
        """Draw maze.

        Args:
            show_path_step (int, optional): If given. Defaults to 0.

        """
        path: list[tuple[int, int]] = self.build_path_cells()
        image = self.mlx.mlx_new_image(self.mlx_ptr, self.maze_width, self.window_height)
        data, _, size_line, _ = self.mlx.mlx_get_data_addr(image)

        self._paint_rect(
            data,
            size_line,
            (0, 0),
            (self.maze_width, self.window_height),
            self.current_colors["CELL_COLOR"],
        )

        grid = self.gen.get_grid()
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                value = grid[row][col]
                x_start = col * self.cell_size
                y_start = row * self.cell_size

                color = None
                if (col, row) == self.gen.config.entry:
                    color = self.current_colors["ENTRY_COLOR"]
                elif (col, row) == self.gen.config.exit:
                    color = self.current_colors["EXIT_COLOR"]
                elif value == MagicValues.CLOSED.value:
                    color = self.current_colors["COLOR_15"]

                if color is not None:
                    self._paint_rect(
                        data, size_line, (x_start, y_start), (self.cell_size, self.cell_size), color
                    )

                wall_color = self.current_colors["WALL_COLOR"]

                if value & MagicValues.NORTH.value:
                    self._paint_rect(
                        data,
                        size_line,
                        (x_start, y_start),
                        (self.cell_size, self.border_size),
                        wall_color,
                    )

                if value & MagicValues.SOUTH.value:
                    self._paint_rect(
                        data,
                        size_line,
                        (x_start, y_start + self.cell_size - self.border_size),
                        (self.cell_size, self.border_size),
                        wall_color,
                    )

                if value & MagicValues.WEST.value:
                    self._paint_rect(
                        data,
                        size_line,
                        (x_start, y_start),
                        (self.border_size, self.cell_size),
                        wall_color,
                    )

                if value & MagicValues.EAST.value:
                    self._paint_rect(
                        data,
                        size_line,
                        (x_start + self.cell_size - self.border_size, y_start),
                        (self.border_size, self.cell_size),
                        wall_color,
                    )

                if show_path_step > 0 and (row, col) in path:
                    idx = path.index((row, col))
                    if idx < show_path_step:
                        mini_size = self.cell_size - 10
                        offset = 10 // 2

                        self._paint_rect(
                            data,
                            size_line,
                            (x_start + offset, y_start + offset),
                            (mini_size, mini_size),
                            self.current_colors["PATH_COLOR"],
                        )

        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, image, 0, 0)

    def draw_menu(self) -> None:
        """Draws the menu."""
        title = "A-maze-ing"
        title_x = self.maze_width // 2 - (len(title) * 10) // 2
        title_y = self.maze_height + 30
        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win_ptr, title_x, title_y, self.current_colors["TEXT_COLOR"], title
        )

        y_pos = self.maze_height + 50
        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            self.maze_width // 2 - (len("1:new maze  2:show path") * 10) // 2,
            y_pos,
            self.current_colors["TEXT_COLOR"],
            "1:new maze  2:show path",
        )

        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            self.maze_width // 2 - (len("3:random colour  ESC:exit") * 10) // 2,
            y_pos + 20,
            self.current_colors["TEXT_COLOR"],
            "3:random colour  ESC:exit",
        )

    def full_redraw(self) -> None:
        """Fully Redraws the maze.

        Clearing the mlx window, drawing the maze and menu again.
        """
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self._draw_maze(0)
        self.draw_menu()

    def render(self) -> None:
        """Render the maze.

        Draws the maze and its menu at start, if a key code is given
        From the accepted keys, executes a command
        """
        self._draw_maze(0)
        self.draw_menu()

        def key_handler(keycode: int, _param: None) -> None:
            """Handle keyboard input.

            Args:
                keycode (int): will be the key code
                _param (None): NECESSARY FOR MLX

            """
            if keycode == Key.ONE.value:  # '1'
                self.is_animating = False
                seed = random.randint(0, 2**32)
                self.gen.config.seed = seed
                gen = MazeGenerator(self.gen.config)
                self.gen = gen
                self.gen.generate()
                self.full_redraw()

            elif keycode == Key.TWO.value:  # '2'
                if self.is_animating:
                    return
                self.path_cells = self.build_path_cells()
                self.path_step = 0
                self.is_animating = True
                self.full_redraw()

            elif keycode == Key.THR.value:  # '3'
                self.apply_new_theme()
                self.is_animating = False
                self.full_redraw()

            elif keycode == Key.FRR.value:  # '4'
                self.is_animating = False

            elif keycode == Key.FVE.value:  # '5'
                self.is_animating = True

            elif keycode == Key.ESC.value:  # ESC
                self.mlx.mlx_loop_exit(self.mlx_ptr)

        def close_window(_empty: None) -> None:
            """Close the window opened by MLX."""
            self.mlx.mlx_loop_exit(self.mlx_ptr)

        self.mlx.mlx_loop_hook(self.mlx_ptr, self.animate_path, None)
        self.mlx.mlx_key_hook(self.win_ptr, key_handler, None)
        self.mlx.mlx_hook(self.win_ptr, 33, 0, close_window, None)

        self.mlx.mlx_loop(self.mlx_ptr)
