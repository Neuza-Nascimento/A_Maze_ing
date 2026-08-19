from mlx.mlx import Mlx


tam = [
    [9, 3, 11, 9, 5, 7, 13, 5, 5, 3, 13, 5, 1, 3, 9, 7, 13, 5, 1, 7],
    [14, 8, 0, 0, 3, 13, 3, 9, 5, 2, 13, 1, 6, 8, 4, 3, 11, 9, 4, 7],
    [11, 10, 14, 14, 14, 13, 2, 12, 7, 12, 1, 6, 11, 10, 13, 0, 2, 8, 5, 7],
    [10, 10, 9, 5, 7, 11, 12, 1, 7, 13, 6, 11, 8, 2, 11, 14, 12, 2, 11, 11],
    [12, 4, 2, 9, 7, 12, 5, 0, 5, 1, 5, 4, 6, 12, 4, 1, 3, 8, 4, 6],
    [9, 5, 4, 0, 5, 3, 15, 10, 15, 10, 15, 15, 15, 11, 11, 14, 14, 10, 11, 11],
    [12, 7, 9, 4, 7, 10, 15, 14, 15, 8, 5, 7, 15, 8, 6, 11, 13, 2, 8, 2],
    [9, 1, 4, 3, 13, 6, 15, 15, 15, 10, 15, 15, 15, 8, 1, 4, 7, 12, 6, 10],
    [14, 14, 13, 2, 11, 13, 5, 3, 15, 14, 15, 13, 5, 6, 10, 13, 1, 5, 3, 10],
    [11, 9, 5, 4, 0, 3, 13, 2, 15, 11, 15, 15, 15, 11, 8, 5, 4, 7, 8, 6],
    [8, 0, 7, 11, 14, 12, 1, 0, 1, 6, 13, 5, 1, 6, 12, 5, 5, 3, 12, 7],
    [10, 14, 9, 4, 5, 7, 10, 14, 10, 9, 3, 11, 8, 7, 11, 13, 1, 4, 1, 3],
    [14, 9, 4, 5, 1, 5, 4, 7, 14, 10, 12, 2, 10, 13, 4, 5, 0, 7, 10, 14],
    [9, 0, 7, 13, 0, 7, 13, 5, 5, 6, 11, 10, 10, 9, 1, 3, 10, 13, 4, 3],
    [14, 12, 7, 13, 4, 5, 5, 5, 5, 5, 4, 4, 4, 6, 14, 12, 6, 13, 5, 6],
]

cores_hex = [
    0xFF000000,  # Preto
    0xFFFFFFFF,  # Branco
    0xFFFF0000,  # Vermelho
    0xFF00FF00,  # Verde
    0xFF0000FF,  # Azul
    0xFFFFFF00,  # Amarelo
    0xFF00FFFF,  # Ciano
    0xFFFF00FF,  # Magenta
    0xFF808080,  # Cinzento
    0xFFFFA500   # Laranja
]

BORDER_COLOR = 0xFFFFFFFF  # Branco para as bordas
BORDER_SIZE = 1  # Tamanho da borda em pixels
ENTRY = (1, 1)
EXIT = (14, 19)


def render() -> None:

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()

    cell_size = 40

    maze_width = len(tam[0]) * cell_size
    maze_height = len(tam) * cell_size
    
    window_height = maze_height + 100

    win_ptr = mlx.mlx_new_window(mlx_ptr, maze_width, window_height, "Array")

    image = mlx.mlx_new_image(mlx_ptr, maze_width, window_height)
    data, bpp, size_line, endian = mlx.mlx_get_data_addr(image)
    bytes_per_pixel = 4

    # Preencher o fundo
    for y in range(window_height):
        for x in range(maze_width):
            pos = y * size_line + x * bytes_per_pixel
            data[pos:pos + 4] = 0xFFFFA500.to_bytes(4, 'little')

    # Desenhar o labirinto com bordas
    for row in range(len(tam)):
        for col in range(len(tam[row])):

            value = tam[row][col]

            if (row, col) == ENTRY:
                color = 0xFF00FF00
            elif (row, col) == EXIT:
                color = 0xFFFF0000
            elif value == 15:
                color = 0xFF00FFFF
            else:
                color = 0xFF000000

            x_start = col * cell_size
            y_start = row * cell_size

            # Desenhar cada célula com borda
            for y in range(cell_size):
                for x in range(cell_size):
                    px = x_start + x
                    py = y_start + y
                    pos = py * size_line + px * bytes_per_pixel

                    # Verificar se estamos na borda da célula
                    is_border = (x < BORDER_SIZE or x >= cell_size - BORDER_SIZE or
                                y < BORDER_SIZE or y >= cell_size - BORDER_SIZE)
                    
                    if is_border:
                        data[pos:pos + 4] = BORDER_COLOR.to_bytes(4, 'little')
                    else:
                        data[pos:pos + 4] = color.to_bytes(4, 'little')

    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image, 0, 0)

    title = "A-maze-ing"
    title_x = maze_width // 2 - (len(title) * 10) // 2
    title_y = maze_height + 30
    mlx.mlx_string_put(
                mlx_ptr, win_ptr, title_x, title_y, 0xFFD700, title)
 
    y_pos = maze_height + 70
    mlx.mlx_string_put(
        mlx_ptr, win_ptr, 10, y_pos, 0xFFFFFF,
        "1:new maze  2:show path  3:random colour  ESC:exit")

    def kew_handler(keycode, param) -> None:
        if keycode == 18:
            print("Pressionou 18: renderizar")
        if keycode == 19:
            print("Pressionou")
        if keycode == 18:
            print("Pressionou")
        if keycode == 18:
            print("Pressionou")

    def close_window(emtpy) -> None:
        mlx.mlx_loop_exit(mlx_ptr)

    mlx.mlx_hook(win_ptr, 33, 0, close_window, None)
    mlx.mlx_hook(win_ptr, 2, 0, kew_handler, None)

    mlx.mlx_loop(mlx_ptr)


render()