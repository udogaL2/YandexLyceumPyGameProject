import pygame
import os
import sys
import random

# ________________________________________
pygame.init()
pygame.display.set_caption('')
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
# ________________________________________

pygame.mixer.music.load(os.path.join('data\music', '001_Synthwave_4k.mp3'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

click_sound = pygame.mixer.Sound(os.path.join('data\music', 'click.ogg'))
click_sound.set_volume(0.4)

win_sound = pygame.mixer.Sound(os.path.join('data\music', 'lvlup.ogg'))
win_sound.set_volume(0.4)

# ________________________________________
# Настройка
clock = pygame.time.Clock()
FPS = 50
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('green')
FONT = pygame.font.Font(None, 36)

# ________________________________________
WIN_STRIKE = [[0] * 5 for _ in range(5)]
CHARACTERS = ['W', 'N', 'J', 'G', 'D', 'A', 'R', 'K', 'L', 'S', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# ________________________________________

player_key = None
levels_completed = []


def load_image(name):
    fullname = os.path.join('data\images', name)
    image = pygame.image.load(fullname)
    return image


pygame.display.set_icon(load_image('плитка 1.png'))
BRICK_COLORS = [load_image('плитка 1.png'), load_image('плитка 3.png')]
SYSTEM_BRICK_COLOR = [load_image('блок.png'), load_image('актив.png')]
TUTORIAL_BG = [load_image('вывод ключа.jpg'), load_image('правила.jpg')]
all_sprites = pygame.sprite.Group()


def generate_key():
    # генерация ключа
    key = ''
    for _ in range(6):
        key += random.choice(CHARACTERS)
    return key[:3] + '-' + key[3:]


def save_game():
    # сохранение пройденных уровней в файл
    global player_key

    fullname = os.path.join('data\saves', player_key + '.txt')
    with open(fullname, 'w') as players_progress:
        players_progress.write(' '.join(levels_completed))
    players_progress.close()


def new_game():
    # создание файла со сгренерированным ключом
    global player_key, levels_completed

    key = generate_key()
    if not os.path.isfile(os.path.join('data\saves', key + '.txt')):
        player_key = key
    else:
        while os.path.isfile(os.path.join('data\saves', key + '.txt')):
            key = generate_key()
        player_key = key

    levels_completed = ['0' for _ in range(16)]

    save_game()


def check_file(key):
    return os.path.isfile(os.path.join('data\saves', key + '.txt'))


def load_preservation(key):
    global player_key, levels_completed

    player_key = key

    fullname = os.path.join('data\saves', player_key + '.txt')
    with open(fullname, 'r') as players_progress:
        levels_completed = [line.split() for line in players_progress][0]
    players_progress.close()


def load_game():
    bg = load_image('загрузка уровня.jpg')
    screen.blit(bg, (0, 0))
    input_box = InputBox(300, 220, 100, 36)
    error = FONT.render("Данный ключ не найден!", True, pygame.Color("white"))

    done = False
    error_flag = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            text = input_box.handle_event(event)
            if text is not None:
                if check_file(text):
                    ok_msg1 = FONT.render("Данный ключ найден!", True, pygame.Color("white"))
                    ok_msg2 = FONT.render("Идет загрузка...", True, pygame.Color("white"))
                    screen.blit(ok_msg1, (270, 300))
                    screen.blit(ok_msg2, (310, 340))
                    pygame.display.flip()
                    load_preservation(text)
                    clock.tick(0)
                    done = True

                else:
                    error_flag = True

            input_box.update()

        if not done:
            screen.blit(bg, (0, 0))
            if error_flag:
                screen.blit(error, (250, 300))
            input_box.render(screen)

            pygame.display.flip()
            clock.tick(FPS)


def load_level(name):
    fullname = os.path.join('data\levels', name)
    with open(fullname, 'r') as mapFile:
        level_map = [list(map(int, line.split())) for line in mapFile]
    mapFile.close()
    return level_map


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    copy = self.text
                    self.text = ''
                    return copy
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def render(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, self.color, self.rect, 2)


class Brick(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.setup(tile_type, pos_x, pos_y)

    def setup(self, color, x, y):
        self.color = int(color)
        self.x = x
        self.y = y
        self.image = BRICK_COLORS[self.color]
        self.rect = self.image.get_rect().move(100 * self.x + 250, 100 * self.y + 50)

    def is_color(self, color):
        return self.color == int(color)

    def get_color(self):
        return self.color

    def switch_color(self):
        self.color = (self.color + 1) % 2
        self.image = BRICK_COLORS[self.color]


class SystemBricks(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.setup(tile_type, pos_x, pos_y)

    def setup(self, color, x, y):
        self.color = int(color)
        self.x = x
        self.y = y
        self.image = SYSTEM_BRICK_COLOR[self.color]
        self.rect = self.image.get_rect().move(100 * self.x + 200, 100 * self.y + 100)


class Board:
    # создание поля
    def __init__(self, width, height, setup):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board_cells = setup[:]
        self.render(setup)
        # значения по умолчанию
        self.left = 250
        self.top = 50
        self.cell_size = 100

    def render(self, setup):
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x] = Brick(setup[y][x], x, y)

    def on_click(self, cell):
        for i in range(5):
            self.board[i][cell[0]].switch_color()
            self.board[cell[1]][i].switch_color()
            self.board_cells[i][cell[0]] = self.board[i][cell[0]].get_color()
            self.board_cells[cell[1]][i] = self.board[cell[1]][i].get_color()
        self.board[cell[1]][cell[0]].switch_color()
        self.board_cells[cell[1]][cell[0]] = self.board[cell[1]][cell[0]].get_color()

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

    def is_win(self):
        return self.board_cells == WIN_STRIKE


def UploadBG(name):
    bg_image = load_image(name)
    bg = pygame.sprite.Sprite(all_sprites)
    bg.image = bg_image
    bg.rect = bg.image.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


class Buttons:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 300
        self.top = 200
        self.cell_size = 100

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            return cell


def tutorial():
    screen.blit(TUTORIAL_BG[0], (0, 0))
    font = pygame.font.Font(None, 60)
    key = font.render(player_key, True, pygame.Color("white"))
    screen.blit(key, (310, 130))
    num_of_click = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                click_sound.play()
                num_of_click += 1
                if num_of_click == 1:
                    screen.blit(TUTORIAL_BG[1], (0, 0))
                elif num_of_click == 2:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    fon = load_image('главное меню.jpg')
    screen.blit(fon, (0, 0))

    buttons = Buttons(2, 3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                tag = buttons.get_click(event.pos)
                if tag is not None:
                    if tag[1] == 0:
                        click_sound.play()
                        new_game()
                        tutorial()
                        return
                    elif tag[1] == 1:
                        click_sound.play()
                        load_game()
                        return
                    elif tag[1] == 2:
                        click_sound.play()
                        terminate()
        pygame.display.flip()
        clock.tick(FPS)


def choose_screen():
    fon = load_image('выбор уровня.jpg')
    screen.blit(fon, (0, 0))

    buttons = Buttons(4, 4)
    buttons.set_view(200, 100, 100)

    quit_button = Buttons(2, 1)
    quit_button.set_view(20, 20, 80)

    for y in range(4):
        for x in range(4):
            screen.blit(SYSTEM_BRICK_COLOR[int(levels_completed[y * 4 + x])], (100 * x + 200, 100 * y + 100))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                click = event.pos
                tag = buttons.get_click(click)
                quit_tag = quit_button.get_click(click)
                if quit_tag is not None:
                    terminate()
                if tag is not None:
                    lvl = tag[0] + 1 + tag[1] * 4
                    return lvl
        pygame.display.flip()
        clock.tick(FPS)


def level_completed_animation():
    tablet = load_image('уровень пройден.png')
    rect = pygame.Rect(0, 0, tablet.get_width() // 5, tablet.get_height())
    for i in range(5):
        frame_location = (rect.w * i, 0)
        screen.blit(tablet.subsurface(pygame.Rect(frame_location, rect.size)), (200, 200))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.time.wait(2000)


def level_window(lvl):
    level_setup = load_level('lvl' + lvl + '.txt')  # загрузка уровня из файла

    fon = load_image('природная тема.jpg')
    screen.blit(fon, (0, 0))

    board = Board(5, 5, level_setup)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if board.is_win():
                win_sound.play()
                level_completed_animation()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                board.get_click(event.pos)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


# ________________________________________________________
start_screen()
# ________________________________________________________

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    num_lvl = str(choose_screen())
    if num_lvl == '1' or levels_completed[int(num_lvl) - 2] == '1':
        level_window(num_lvl)
        levels_completed[int(num_lvl) - 1] = '1'
    else:
        pass
        # ошибка
    clock.tick(FPS)
    save_game()

pygame.quit()
