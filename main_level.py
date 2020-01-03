import pygame
import os
import sys

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
FPS = 50


def load_image(name):
    fullname = os.path.join('images', name)
    fullname = os.path.join('data', fullname)
    image = pygame.image.load(fullname)
    return image


colors = [load_image('плитка 1.png'), load_image('плитка 3.png')]


class Brick(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = colors[tile_type]
        self.rect = self.image.get_rect().move(100 * pos_x + 250, 100 * pos_y + 50)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        # self.board[y][x]]
        for y in range(self.height):
            for x in range(self.width):
                Brick(self.board[y][x], x, y)

    def on_click(self, cell):
        for i in range(self.height):
            self.board[i][cell[0]] = (self.board[i][cell[0]] + 1) % 2
        for i in range(self.width):
            self.board[cell[1]][i] = (self.board[cell[1]][i] + 1) % 2
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


board = Board(5, 5)
board.set_view(250, 50, 100)
bg_image = load_image('природная тема.jpg')
all_sprites = pygame.sprite.Group()
bg = pygame.sprite.Sprite(all_sprites)
bg.image = bg_image
bg.rect = bg.image.get_rect()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    all_sprites.draw(screen)
    board.render()
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
