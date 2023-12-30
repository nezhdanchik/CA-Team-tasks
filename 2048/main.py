import time

import pygame as pg
import numpy as np
import random


class Square(pg.sprite.Sprite):
    size = 0
    margin = 5

    def __init__(self, screen, color, x, y, field_coordinates):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.color = color
        self.image = pg.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = pg.Rect(x, y, self.size, self.size)
        self.x = x
        self.y = y
        self.field_coordinates = field_coordinates  # координаты ячейки в игровом поле (индексы)


class Cell(Square):
    """
    Ячейка игрового поля. Неподвижная часть игрового поля. Хранит информацию о свободных ячейках.
    """
    all_cells = pg.sprite.Group()

    def __init__(self, screen, color, x, y, field_coordinates, is_free):
        super().__init__(screen, color, x, y, field_coordinates)
        self.is_free = is_free
        self.block_in_cell = None
        self.all_cells.add(self)  # добавляем ячейку в группу для дальнейшего управления

    @classmethod
    def find_free_cells(cls):
        free_cells = []
        for cell in cls.all_cells:
            if cell.is_free:
                free_cells.append(cell)
        if len(free_cells) == 0:
            print('Игра окончена')
            pg.quit()
            exit()
        return free_cells

    def update(self, *args, **kwargs):
        self.screen.blit(self.image, self.rect)


class Block(Square):
    all_blocks = pg.sprite.Group()

    colors = {
        2: (213, 189, 175),
        4: (214, 176, 203),
        8: (237, 224, 200),  # Light Yellow
        16: (255, 255, 224),  # Light Yellow
        32: (240, 248, 255),  # Alice Blue
        64: (255, 240, 245),  # Lavender Blush
        128: (245, 255, 250),  # Mint Cream
        256: (240, 255, 240),  # Honeydew
        512: (255, 228, 196),  # Bisque
        1024: (240, 255, 255),  # Azure
        2048: (255, 250, 250),  # Snow
        4096: (255, 239, 219),  # Peach Puff
        8192: (255, 228, 225),  # Misty Rose
        16384: (240, 248, 255),  # Alice Blue
        32768: (255, 240, 245),  # Lavender Blush
        65536: (245, 255, 250),  # Mint Cream
        131072: (240, 255, 240),  # Honeydew
        262144: (255, 228, 196),  # Bisque
        524288: (240, 255, 255),  # Azure
        1048576: (255, 250, 250),  # Snow
    }

    def __init__(self, screen, color, x, y, field_coordinates, points):
        super().__init__(screen, color, x, y, field_coordinates)
        self.points = points  #
        self.color = Block.colors[points]
        pg.font.init()
        self.font = pg.font.SysFont("Arial", int(Square.size * 0.6))
        self.all_blocks.add(self)

    def del_block(self):
        Block.all_blocks.remove(self)

    def move(self, direction_x, direction_y):
        # текущее положение относительно поля
        curr_x, curr_y = self.field_coordinates
        # если не выходит за границы поля
        if 0 <= curr_x + direction_x < Game.count_cells and 0 <= curr_y + direction_y < Game.count_cells:
            new_x, new_y = curr_x + direction_x, curr_y + direction_y
            if Field.field[new_y][new_x].is_free:
                Field.field[curr_y][curr_x].is_free = True
                Field.field[new_y][new_x].is_free = False
                Field.field[new_y][new_x].block_in_cell = self
                self.field_coordinates = new_x, new_y
                self.rect = Field.field[new_y][new_x].rect
            else:
                cell_before = Field.field[new_y][new_x]
                if cell_before.block_in_cell.points == self.points:
                    # произойдет слияние блоков
                    Field.field[curr_y][curr_x].is_free = True
                    cell_before.block_in_cell.points *= 2
                    cell_before.block_in_cell.color = Block.colors[cell_before.block_in_cell.points]
                    Block.all_blocks.remove(self)
                    return -1 # слияние произошло


    @classmethod
    def move_all(cls, direction):
        stop = False # если произойдёт слияние, надо выйти из цикла
        if direction == 'right':
            for row in Field.field:
                for cell in row[::-1]:
                    if not cell.is_free:
                        if cell.block_in_cell.move(1, 0) == -1:
                            stop = True
        elif direction == 'left':
            for row in Field.field:
                for cell in row:
                    if not cell.is_free:
                        if cell.block_in_cell.move(-1, 0) == -1:
                            stop = True
        elif direction == 'up':
            for ind_collumn in range(Game.count_cells):
                collumn = Field.field[:, ind_collumn]
                for cell in collumn:
                    if not cell.is_free:
                        if cell.block_in_cell.move(0, -1) == -1:
                            stop = True
        elif direction == 'down':
            for ind_collumn in range(Game.count_cells):
                collumn = Field.field[:, ind_collumn]
                for cell in collumn[::-1]:
                    if not cell.is_free:
                        if cell.block_in_cell.move(0, 1) == -1:
                            stop = True
        return stop

    def update(self, *args, **kwargs):
        self.image.fill(self.color)
        textSurf = self.font.render(str(self.points), True, (0, 0, 0))
        self.image.blit(textSurf,
                        [Square.size / 2 - textSurf.get_width() / 2, Square.size / 2 - textSurf.get_height() / 2])
        self.screen.blit(self.image, self.rect)


class Field:
    field = None

    def __init__(self, screen, screen_info):
        # размер игрового поля
        self.screen = screen
        self.screen_info = screen_info
        self.block = None  # здесь будет храниться блок
        # здесь будет храниться игровое поле
        Field.field = np.array([[0] * Game.count_cells for _ in range(Game.count_cells)], dtype=Cell)

        self.create_cells(pg.Color('0xf5ebe0'))
        Cell.all_cells.update()

        self.spawn_block(pg.Color('0xd5bdaf'), 2)
        Block.all_blocks.update()

    def create_cells(self, color):
        # длина всего поля
        n = Cell.size * Game.count_cells + Cell.margin * (Game.count_cells - 1)
        # координаты левого верхнего угла
        x_start, y_start = self.screen_info['center'][0] - n // 2, self.screen_info['center'][1] - n // 2
        # рисуем все ячейки
        for y in range(Game.count_cells):
            for x in range(Game.count_cells):
                new_cell = Cell(self.screen, color, x_start + x * (Cell.size + Cell.margin),
                                y_start + y * (Cell.size + Cell.margin), (x, y), True)
                self.field[y][x] = new_cell

    def spawn_block(self, color, count=1):
        # выбираем случайную свободную ячейку
        for i in range(count):
            free_cells = Cell.find_free_cells()
            cell = random.choice(free_cells)
            cell.is_free = False
            b = Block(self.screen, color, cell.x, cell.y, cell.field_coordinates, random.choice([2, 2, 2, 2, 4]))
            cell.block_in_cell = b


class Game:
    count_cells = None

    def __init__(self, count_cells, resolution=0):
        pg.init()
        Game.count_cells = count_cells
        self.background_color = pg.Color('0xd6ccc2')
        if resolution == 0:
            self.screen = pg.display.set_mode()
        else:
            self.screen = pg.display.set_mode((resolution, resolution))
        self.screen.fill(self.background_color)
        self.width, self.height = self.screen.get_size()
        self.center = self.width // 2, self.height // 2

        # определение лучшего размера ячейки
        # -50 - отступы от краев экрана; 5 * (count_cells - 1) - отступы между ячейками
        Square.size = (min(self.width, self.height) - 50 - Cell.margin * (count_cells - 1)) // count_cells


        Square.count_cells = count_cells
        # создание игрового поля
        screen_info = {'width': self.width, 'height': self.height, 'center': self.center}
        self.board = Field(self.screen, screen_info)

        self.clock = pg.time.Clock()
        self.run()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.KEYDOWN:
                    for i in range(Game.count_cells):
                        stop = False
                        if event.key == pg.K_UP:
                            stop = Block.move_all('up')
                        elif event.key == pg.K_DOWN:
                            stop = Block.move_all('down')
                        elif event.key == pg.K_LEFT:
                            stop = Block.move_all('left')
                        elif event.key == pg.K_RIGHT:
                            stop = Block.move_all('right')

                        if stop:  # где-то произошло слияние блоков
                            break

                        Cell.all_cells.update()
                        Block.all_blocks.update()
                        pg.display.flip()
                        time.sleep(0.025)

                    self.board.spawn_block(pg.Color('0xd5bdaf'), 1)

            Cell.all_cells.update()
            Block.all_blocks.update()

            pg.display.flip()
            self.clock.tick(60)

    def __del__(self):
        pg.quit()


while True:
    n = int(input('Размер поля: 2 <= n <= 50 '))
    if not 2 <= n <= 50:
        print('Неверное значение n; 2 <= n <= 50')
        continue
    resolution = int(input('Разрешение экрана: (Введите 0, если хотите во весь экран) ? '))
    g = Game(n, resolution=resolution)
    break