from mlx.mlx import Mlx
from enum import Enum
import random

# ============================================================
# DADOS DO LABIRINTO
# ============================================================
tam = [
    [9, 7, 9, 3, 9, 5, 5, 5, 3, 9, 3, 9, 5, 5, 5, 5, 1, 3, 9, 7],
    [10, 13, 6, 10, 12, 3, 9, 3, 10, 14, 12, 2, 11, 9, 5, 5, 6, 10, 8, 3],
    [10, 9, 3, 12, 3, 12, 6, 10, 12, 5, 3, 12, 6, 10, 13, 1, 7, 10, 14, 10],
    [10, 10, 12, 3, 10, 9, 3, 12, 3, 11, 12, 5, 3, 8, 3, 12, 3, 12, 5, 2],
    [12, 4, 7, 10, 12, 6, 12, 1, 6, 8, 5, 5, 6, 10, 10, 9, 4, 5, 7, 10],
    [9, 3, 9, 0, 5, 7, 15, 10, 15, 10, 15, 15, 15, 14, 10, 8, 5, 3, 9, 6],
    [10, 12, 6, 14, 9, 3, 15, 14, 15, 8, 5, 7, 15, 9, 6, 12, 3, 10, 12, 3],
    [10, 9, 3, 9, 6, 10, 15, 15, 15, 10, 15, 15, 15, 10, 11, 9, 6, 12, 5, 6],
    [10, 10, 12, 6, 9, 6, 9, 3, 15, 10, 15, 13, 5, 2, 12, 2, 9, 5, 3, 11],
    [10, 10, 9, 7, 12, 5, 6, 10, 15, 10, 15, 15, 15, 12, 3, 12, 6, 9, 6, 10],
    [12, 4, 2, 9, 5, 5, 3, 8, 3, 12, 3, 9, 1, 5, 6, 9, 7, 10, 9, 2],
    [9, 3, 14, 12, 3, 11, 12, 6, 10, 9, 6, 10, 10, 9, 1, 6, 9, 6, 10, 10],
    [10, 12, 5, 5, 6, 8, 5, 5, 6, 12, 3, 14, 10, 10, 12, 3, 12, 5, 6, 10],
    [8, 3, 13, 5, 5, 6, 9, 5, 5, 3, 12, 5, 6, 10, 11, 12, 3, 9, 5, 6],
    [14, 12, 5, 5, 5, 5, 4, 5, 7, 12, 5, 5, 5, 4, 4, 7, 12, 4, 5, 7],
]
ENTRY = (0, 0)
EXIT = (14, 19)
SOL = "SSSSENNESESSWSWNWSSSSSENNNESENENESSWSEENESSSWNWWWSESWWWNWSSESEEEEENEEESEEEENNNESESESEEE"

# ============================================================
# CONSTANTES DO LABIRINTO
# ============================================================
BORDER_SIZE = 1
NORTH = 0b0001  # 1
EAST = 0b0010   # 2
SOUTH = 0b0100  # 4
WEST = 0b1000   # 8


# ============================================================
# CORES PADRÃO (serão substituídas pelas aleatórias)
# ============================================================
WALL_COLOR = 0xFF14213D
PATH_COLOR = 0xFF48CAE4
ENTRY_COLOR = 0xFF52B788
EXIT_COLOR = 0xFFE76F51
BORDER_COLOR = 0xFF4A6072
CELL_COLOR = 0xFFE8F1F2
TEXT_COLOR = 0xFF14213D
COLOR_15 = 0xFFFFC857

# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================
current_colors = {
    "WALL_COLOR": WALL_COLOR,
    "PATH_COLOR": PATH_COLOR,
    "ENTRY_COLOR": ENTRY_COLOR,
    "EXIT_COLOR": EXIT_COLOR,
    "BORDER_COLOR": BORDER_COLOR,
    "CELL_COLOR": CELL_COLOR,
    "TEXT_COLOR": TEXT_COLOR,
    "COLOR_15": COLOR_15,
}

path_cells = []       # Lista de células do caminho
path_step = 0         # Quantas células já foram reveladas
is_animating = False  # Se a animação está rodando

def load_images():
    global img_bg, img_entry, img_exit, img_walker

    # Imagem de fundo (ex: textura de pedra, pergaminho, etc.)
    img_bg_data, w, h = mlx.mlx_png_file_to_image(mlx_ptr, "aa1.png")
    img_bg = {"img": img_bg_data, "w": w, "h": h}

    # Ícone de entrada
    # img_entry_data, w, h = mlx.mlx_png_file_to_image(mlx_ptr, "Instagram_logo_2022.svg")
    # img_entry = {"img": img_entry_data, "w": w, "h": h}

    # # Ícone de saída
    # img_exit_data, w, h = mlx.mlx_png_file_to_image(mlx_ptr, "Instagram_logo_2022.svg")
    # img_exit = {"img": img_exit_data, "w": w, "h": h}

    # # Sprite do "andarilho" que percorre o caminho
    # img_walker_data, w, h = mlx.mlx_png_file_to_image(mlx_ptr, "Instagram_logo_2022.svg")
    # img_walker = {"img": img_walker_data, "w": w, "h": h}

def full_redraw(maze_height):
    mlx.mlx_clear_window(mlx_ptr, win_ptr)
    draw_maze(mlx, mlx_ptr, win_ptr, maze_width, window_height, cell_size, 0)
    draw_menu(mlx, mlx_ptr, win_ptr, maze_width, maze_height)

def random_color(min_r, max_r, min_g, max_g, min_b, max_b):
    """Gera uma cor RGB aleatória dentro dos intervalos especificados"""
    r = random.randint(min_r, max_r)
    g = random.randint(min_g, max_g)
    b = random.randint(min_b, max_b)
    # Formato ARGB (0xFF = alpha total)
    return (0xFF << 24) | (r << 16) | (g << 8) | b

def generate_color_palette():
    """Gera uma paleta de cores aleatória"""
    return {
        "WALL_COLOR": random_color(10, 50, 10, 50, 10, 50),       # Cores escuras
        "PATH_COLOR": random_color(100, 200, 150, 255, 100, 200),  # Cores claras/vibrantes
        "ENTRY_COLOR": random_color(50, 150, 150, 255, 80, 180),   # Tons verdes/azuis
        "EXIT_COLOR": random_color(200, 255, 50, 150, 50, 150),    # Tons avermelhados
        "BORDER_COLOR": random_color(60, 120, 60, 120, 60, 120),   # Cores médias
        "CELL_COLOR": random_color(200, 255, 200, 255, 200, 255),  # Cores bem claras
        "TEXT_COLOR": random_color(10, 50, 10, 50, 10, 50),        # Cores escuras
        "COLOR_15": random_color(200, 255, 180, 240, 50, 150),     # Tons amarelados
    }

# Gerar 5 temas diferentes
COLORS_THEMES = [generate_color_palette() for _ in range(5)]
current_theme_index = 0

# ============================================================
# FUNÇÃO PARA CONSTRUIR O CAMINHO
# ============================================================
DIR_BY_LETTER = {
    "N": (-1, 0),   # linha -1
    "S": (1, 0),    # linha +1
    "E": (0, 1),    # coluna +1
    "W": (0, -1),   # coluna -1
}

def build_path_cells(entry: tuple[int, int], path_sol: str) -> list[tuple[int, int]]:
    path: list[tuple[int, int]] = []
    row, col = entry
    path.append((row, col))

    for letter in path_sol:
        dr, dc = DIR_BY_LETTER[letter]
        row += dr
        col += dc
        path.append((row, col))

    return path

# ============================================================
# FUNÇÃO PARA DESENHAR O LABIRINTO
# ============================================================
def draw_maze(mlx, mlx_ptr, win_ptr, maze_width, window_height, cell_size, show_path_step=0):
    """
    Desenha o labirinto
    show_path_step: quantas células do caminho mostrar (0 = nenhuma)
    """
    global current_colors
    
    # Construir caminho completo
    path = build_path_cells(ENTRY, SOL)
    
    image = mlx.mlx_new_image(mlx_ptr, maze_width, window_height)
    data, bpp, size_line, endian = mlx.mlx_get_data_addr(image)
    bytes_per_pixel = 4
    for y in range(window_height):
        for x in range(maze_width):
            pos = y * size_line + x * bytes_per_pixel
            data[pos:pos + 4] = current_colors["CELL_COLOR"].to_bytes(4, 'little')

    # Desenhar o labirinto
    for row in range(len(tam)):
        for col in range(len(tam[row])):

            value = tam[row][col]
            x_start = col * cell_size
            y_start = row * cell_size

            # Desenhar a célula base (entrada, saída, caminho ou parede)
            color = None
            if (row, col) == ENTRY:
                color = current_colors["ENTRY_COLOR"]
            elif (row, col) == EXIT:
                color = current_colors["EXIT_COLOR"]
            elif value == 15:
                color = current_colors["COLOR_15"]
            else:
                # Célula normal (sem cor específica)
                pass
            
            if color is not None:
                for y in range(cell_size):
                    for x in range(cell_size):
                        px = x_start + x
                        py = y_start + y
                        pos = py * size_line + px * bytes_per_pixel
                        data[pos:pos + 4] = color.to_bytes(4, 'little')

            # Desenhar paredes
            if value & NORTH:
                for x in range(cell_size):
                    for y in range(BORDER_SIZE):
                        px = x_start + x
                        py = y_start + y
                        pos = py * size_line + px * bytes_per_pixel
                        data[pos:pos + 4] = current_colors["WALL_COLOR"].to_bytes(4, 'little')
            
            if value & SOUTH:
                for x in range(cell_size):
                    for y in range(cell_size - BORDER_SIZE, cell_size):
                        px = x_start + x
                        py = y_start + y
                        pos = py * size_line + px * bytes_per_pixel
                        data[pos:pos + 4] = current_colors["WALL_COLOR"].to_bytes(4, 'little')
            
            if value & WEST:
                for y in range(cell_size):
                    for x in range(BORDER_SIZE):
                        px = x_start + x
                        py = y_start + y
                        pos = py * size_line + px * bytes_per_pixel
                        data[pos:pos + 4] = current_colors["WALL_COLOR"].to_bytes(4, 'little')
            
            if value & EAST:
                for y in range(cell_size):
                    for x in range(cell_size - BORDER_SIZE, cell_size):
                        px = x_start + x
                        py = y_start + y
                        pos = py * size_line + px * bytes_per_pixel
                        data[pos:pos + 4] = current_colors["WALL_COLOR"].to_bytes(4, 'little')

            if show_path_step > 0 and (row, col) in path:
                idx = path.index((row, col))
                if idx < show_path_step:
                    path_color = current_colors["PATH_COLOR"]

                    inset = 10  # quanto menor que a célula
                    mini_size = cell_size - inset
                    offset = inset // 2  # desloca para centralizar

                    for y in range(mini_size):
                        for x in range(mini_size):
                            px = x_start + offset + x
                            py = y_start + offset + y
                            pos = py * size_line + px * bytes_per_pixel

                            is_border = (x < BORDER_SIZE or x >= mini_size - BORDER_SIZE or
                                        y < BORDER_SIZE or y >= mini_size - BORDER_SIZE)

                            if is_border:
                                data[pos:pos + 4] = path_color.to_bytes(4, 'little')
                            else:
                                data[pos:pos + 4] = path_color.to_bytes(4, 'little')

    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image, 0, 0)

# ============================================================
# FUNÇÃO PARA DESENHAR O MENU
# ============================================================
def draw_menu(mlx, mlx_ptr, win_ptr, maze_width, maze_height) -> None:
    global current_colors
    
    title = "A-maze-ing"
    title_x = maze_width // 2 - (len(title) * 10) // 2
    title_y = maze_height + 30
    mlx.mlx_string_put(
                mlx_ptr, win_ptr, title_x, title_y, 0xFFD700, title)

    y_pos = maze_height + 70
    mlx.mlx_string_put(
        mlx_ptr, win_ptr, 10, y_pos, current_colors["TEXT_COLOR"],
        "1:new maze  2:show path  3:random colour  ESC:exit")

# ============================================================
# FUNÇÃO DE ANIMAÇÃO DO CAMINHO
# ============================================================
def animate_path(param):
    """Função chamada automaticamente para animar o caminho"""
    global path_step, is_animating, path_cells
    
    if not is_animating:
        return
    
    if path_step >= len(path_cells):
        is_animating = False
        return
    
    # Avançar uma célula
    path_step += 1
    mlx.mlx_clear_window(mlx_ptr, win_ptr)
    # Redesenhar com o novo passo
    draw_maze(mlx, mlx_ptr, win_ptr, maze_width, window_height, cell_size, path_step)
    # draw_menu(mlx, mlx_ptr, win_ptr, maze_width, maze_height)
# ============================================================
# FUNÇÃO PARA APLICAR NOVO TEMA DE CORES
# ============================================================
def apply_new_theme():
    """Aplica um novo tema de cores aleatório"""
    global current_colors, current_theme_index
    
    # Avançar para o próximo tema (ciclo)
    current_theme_index = (current_theme_index + 1) % len(COLORS_THEMES)
    current_colors = COLORS_THEMES[current_theme_index].copy()

# ============================================================
# FUNÇÃO PRINCIPAL RENDER
# ============================================================
def render() -> None:
    global mlx, mlx_ptr, win_ptr, maze_width, window_height, cell_size
    global path_cells, path_step, is_animating

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()

    cell_size = 30

    maze_width = len(tam[0]) * cell_size
    maze_height = len(tam) * cell_size
    window_height = maze_height + 100

    win_ptr = mlx.mlx_new_window(mlx_ptr, maze_width, window_height, "A-maze-ing")

    load_images()

    # Desenhar labirinto inicial
    draw_maze(mlx, mlx_ptr, win_ptr, maze_width, window_height, cell_size, 0)
    draw_menu(mlx, mlx_ptr, win_ptr, maze_width, maze_height)

    # ============================================================
    # HANDLER DE TECLAS
    # ============================================================
    def key_handler(keycode, param) -> None:
        global path_cells, path_step, is_animating, current_colors

        print(f"Tecla {keycode}")

        if keycode == 49:  # '1'
            is_animating = False
            full_redraw(maze_height)

        elif keycode == 50:  # '2'
            print(" Mostrar caminho...")
            if is_animating:
                return
            path_cells = build_path_cells(ENTRY, SOL)
            path_step = 0
            is_animating = True
            full_redraw(maze_height)

        elif keycode == 51:  # '3'
            apply_new_theme()
            is_animating = False
            full_redraw(maze_height)

        elif keycode == 65307:  # ESC
            mlx.mlx_loop_exit(mlx_ptr)

    def close_window(empty) -> None:
        mlx.mlx_loop_exit(mlx_ptr)

    # ============================================================
    # REGISTRAR HOOKS
    # ============================================================
    mlx.mlx_loop_hook(mlx_ptr, animate_path, None)  # Hook da animação
    mlx.mlx_key_hook(win_ptr, key_handler, None)    # Hook das teclas
    mlx.mlx_hook(win_ptr, 33, 0, close_window, None) # Hook de fechar janela

    # ============================================================
    # LOOP PRINCIPAL
    # ============================================================
    mlx.mlx_loop(mlx_ptr)


# ============================================================
# EXECUTAR
# ============================================================
if __name__ == "__main__":
    render()