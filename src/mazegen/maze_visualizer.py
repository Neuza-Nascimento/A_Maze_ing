import random

from lib.mlx import Mlx

from .magic_values import DIR_BY_LETTER, Key, MagicValues
from .maze_generator import MazeGenerator


class MazeVisualizer:
    """Display visual representation of the generated maze by the mazeGenerator Class"""

    def __init__(self, generator: MazeGenerator) -> None:
        self.gen = generator
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.cell_size = 30
        self.maze_height = self.gen.get_height() * self.cell_size
        self.maze_width = self.gen.get_width() * self.cell_size
        self.window_height = self.maze_height + 100
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.maze_width, self.window_height, "A-maze-ing"
        )
        self.color_themes = [self.generate_color_palette() for _ in range(5)]
        self.current_theme_index = 0
        self.current_colors = self.color_themes[self.current_theme_index].copy()
        self.border_size = 1
        self.path_cells = []
        self.path_step = 0
        self.is_animating = False

    def random_color(   # PODE SER UM METODO ESTATICO E OS ARGUMENTOS PODEM SER TUPLAS
        self, min_r: int, max_r: int, min_g: int, max_g: int, min_b: int, max_b: int
    ) -> int:
        r = random.randint(min_r, max_r)
        g = random.randint(min_g, max_g)
        b = random.randint(min_b, max_b)
        return (0xFF << 24) | (r << 16) | (g << 8) | b

    def generate_color_palette(self) -> dict[str, int]:
        return {
            "WALL_COLOR": self.random_color(10, 50, 10, 50, 10, 50),
            "PATH_COLOR": self.random_color(100, 200, 150, 255, 100, 200),
            "ENTRY_COLOR": self.random_color(50, 150, 150, 255, 80, 180),
            "EXIT_COLOR": self.random_color(200, 255, 50, 150, 50, 150),
            "BORDER_COLOR": self.random_color(60, 120, 60, 120, 60, 120),
            "CELL_COLOR": self.random_color(200, 255, 200, 255, 200, 255),
            "TEXT_COLOR": self.random_color(10, 50, 10, 50, 10, 50),
            "COLOR_15": self.random_color(200, 255, 180, 240, 50, 150),
        }

    def apply_new_theme(self) -> None:
        self.current_theme_index: int = (self.current_theme_index + 1) % len(self.color_themes)
        self.current_colors: dict[str, int] = self.color_themes[self.current_theme_index].copy()

    def build_path_cells(self) -> list[tuple[int, int]]:
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

    def animate_path(self, _param) -> None:  # DEFINIR TIPO
        if not self.is_animating:
            return

        if self.path_step >= len(self.path_cells):
            self.is_animating = False
            return

        self.path_step += 1
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self._draw_maze(self.path_step)
        self.draw_menu()

    # FUNÇÃO COMPLEXA DMS
    def _draw_maze(self, show_path_step: int = 0) -> None:

        path = self.build_path_cells()

        image = self.mlx.mlx_new_image(self.mlx_ptr, self.maze_width, self.window_height)
        data, _bpp, size_line, _endian = self.mlx.mlx_get_data_addr(image)
        bytes_per_pixel = 4
        current_colors = self.current_colors

        for y in range(self.window_height):
            for x in range(self.maze_width):
                pos = y * size_line + x * bytes_per_pixel
                data[pos: pos + 4] = current_colors["CELL_COLOR"].to_bytes(4, "little")

        grid = self.gen.get_grid()
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                value = grid[row][col]
                x_start = col * self.cell_size
                y_start = row * self.cell_size

                color = None
                if (col, row) == self.gen.config.entry:
                    color = current_colors["ENTRY_COLOR"]
                elif (col, row) == self.gen.config.exit:
                    color = current_colors["EXIT_COLOR"]
                elif value == MagicValues.CLOSED.value:  # 15
                    color = current_colors["COLOR_15"]

                if color is not None:
                    for y in range(self.cell_size):
                        for x in range(self.cell_size):
                            px = x_start + x
                            py = y_start + y
                            pos = py * size_line + px * bytes_per_pixel
                            data[pos: pos + 4] = color.to_bytes(4, "little")

                if value & MagicValues.NORTH.value:
                    for x in range(self.cell_size):
                        for y in range(self.border_size):
                            px = x_start + x
                            py = y_start + y
                            pos = py * size_line + px * bytes_per_pixel
                            data[pos: pos + 4] = current_colors["WALL_COLOR"].to_bytes(4, "little")

                if value & MagicValues.SOUTH.value:
                    for x in range(self.cell_size):
                        for y in range(self.cell_size - self.border_size, self.cell_size):
                            px = x_start + x
                            py = y_start + y
                            pos = py * size_line + px * bytes_per_pixel
                            data[pos: pos + 4] = current_colors["WALL_COLOR"].to_bytes(4, "little")

                if value & MagicValues.WEST.value:
                    for y in range(self.cell_size):
                        for x in range(self.border_size):
                            px = x_start + x
                            py = y_start + y
                            pos = py * size_line + px * bytes_per_pixel
                            data[pos: pos + 4] = current_colors["WALL_COLOR"].to_bytes(4, "little")

                if value & MagicValues.EAST.value:
                    for y in range(self.cell_size):
                        for x in range(self.cell_size - self.border_size, self.cell_size):
                            px = x_start + x
                            py = y_start + y
                            pos = py * size_line + px * bytes_per_pixel
                            data[pos: pos + 4] = current_colors["WALL_COLOR"].to_bytes(4, "little")

                if show_path_step > 0 and (row, col) in path:
                    idx = path.index((row, col))
                    if idx < show_path_step:
                        path_color = current_colors["PATH_COLOR"]

                        inset = 10
                        mini_size = self.cell_size - inset
                        offset = inset // 2

                        for y in range(mini_size):
                            for x in range(mini_size):
                                px = x_start + offset + x
                                py = y_start + offset + y
                                pos = py * size_line + px * bytes_per_pixel

                                is_border = (
                                    x < self.border_size
                                    or x >= mini_size - self.border_size
                                    or y < self.border_size
                                    or y >= mini_size - self.border_size
                                )

                                if is_border:
                                    data[pos: pos + 4] = path_color.to_bytes(4, "little")
                                else:
                                    data[pos: pos + 4] = path_color.to_bytes(4, "little")

        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, image, 0, 0)

    def draw_menu(self) -> None:

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
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self._draw_maze(0)
        self.draw_menu()

    def render(self) -> None:
        self._draw_maze(0)
        self.draw_menu()

        def key_handler(keycode: int, _param) -> None:  # DEFINIR TIPO

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

        def close_window(_empty) -> None:    # DEFINIR TIPO
            self.mlx.mlx_loop_exit(self.mlx_ptr)

        self.mlx.mlx_loop_hook(self.mlx_ptr, self.animate_path, None)
        self.mlx.mlx_key_hook(self.win_ptr, key_handler, None)
        self.mlx.mlx_hook(self.win_ptr, 33, 0, close_window, None)

        self.mlx.mlx_loop(self.mlx_ptr)
