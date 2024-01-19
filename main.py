import sqlite3
import sys
import pygame
import math
import random
import time


pygame.init()

screen_width = 700
screen_height = 700
target_fps = 60
cell_size_px = 90
img_size_px = 75
origin = (0, 0)
grid_color = (100, 100, 100)

screen = pygame.display.set_mode(size=(screen_width, screen_height), flags=pygame.SRCALPHA)
pygame.display.set_caption('Выберите режим игры')

running = True
game_type = None
drag_prev = None

# Стартовое окно

font = pygame.font.Font(None, 32)

'''Отрисовка стартового окна. Отображаются кнопки выбора режима и истории'''
def draw_start_window():
    global button1, button2, button3
    screen.fill((255, 255, 255))

    text = font.render("Выберите режим игры", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(text, text_rect)

    button1 = pygame.Rect(screen_width // 2 - 125, screen_height // 2, 250, 50)
    pygame.draw.rect(screen, (0, 0, 0), button1)
    text = font.render("человек с роботом", True, (255, 255, 255))
    text_rect = text.get_rect(center=button1.center)
    screen.blit(text, text_rect)

    button2 = pygame.Rect(screen_width // 2 - 125, screen_height // 2 + 70, 250, 50)
    pygame.draw.rect(screen, (0, 0, 0), button2)
    text = font.render("человек с человеком", True, (255, 255, 255))
    text_rect = text.get_rect(center=button2.center)
    screen.blit(text, text_rect)

    button3 = pygame.Rect(screen_width - 260, 10, 250, 50)
    pygame.draw.rect(screen, (0, 0, 0), button3)
    text = font.render("История игр", True, (255, 255, 255))
    text_rect = text.get_rect(center=button3.center)
    screen.blit(text, text_rect)

    pygame.display.flip()


def open_table():
    pressed = True
    while pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pressed = False
                break

    '''Открытие и чтение бд'''
    con = sqlite3.connect('./files/data/wins_story.db')
    cursor = con.cursor()

    cursor.execute("SELECT * FROM story")
    rows = cursor.fetchall()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                con.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_btn.collidepoint(event.pos):
                    con.close()
                    return

        draw_table(rows)
        pygame.display.update()




def draw_table(rows):
    global exit_btn
    screen.fill((255, 255, 255))

    font = pygame.font.SysFont(None, 30)
    title_type = font.render("Тип игры", True, (0, 0, 0))
    title_winner = font.render("Победитель", True, (0, 0, 0))
    title_time = font.render("Время", True, (0, 0, 0))
    screen.blit(title_type, (50, 100))
    screen.blit(title_winner, (300, 100))
    screen.blit(title_time, (500, 100))

    exit_btn = pygame.Rect(screen_width - 260, 10, 250, 50)
    pygame.draw.rect(screen, (0, 0, 0), exit_btn)
    text = font.render("Выход", True, (255, 255, 255))
    text_rect = text.get_rect(center=exit_btn.center)
    screen.blit(text, text_rect)

    font = pygame.font.SysFont(None, 24)
    y = 150
    for row in rows:
        type_text = font.render(row[0], True, (0, 0, 0))
        winner_text = font.render(row[1], True, (0, 0, 0))
        time_text = font.render(row[2], True, (0, 0, 0))
        screen.blit(type_text, (50, y))
        screen.blit(winner_text, (300, y))
        screen.blit(time_text, (500, y))
        y += 30


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button1.collidepoint(event.pos):
                game_type = "человек с роботом"
                running = False
            elif button2.collidepoint(event.pos):
                game_type = "человек с человеком"
                running = False

            elif button3.collidepoint(event.pos):
                open_table()

    draw_start_window()

running = True

# Стартовая анимация

f1 = pygame.font.Font('./files/fonts/mr_countryhouseg_0.ttf', 50)
text1 = f1.render("New Year's Tic Tac Toe", True, (180, 0, 0))
text_rect = text1.get_rect(center=(screen_width/2, screen_height/2))
ghost_alpha = round(255 * 0.35)

snowflake_image = pygame.image.load("./files/img/snowflake.jpg")
snowflake_scale_x = snowflake_image.get_width() / snowflake_image.get_height()
snowflake_scale_y = 1
snowflake_image = pygame.transform.smoothscale(snowflake_image,
    (round(img_size_px * snowflake_scale_x), round(img_size_px * snowflake_scale_y)))

snowflake_image_transparent = pygame.Surface((snowflake_image.get_width(), snowflake_image.get_height()))
snowflake_image_transparent.blit(snowflake_image, (0, 0))
snowflake_image_transparent.set_alpha(ghost_alpha)

ball_image = pygame.image.load("./files/img/ball.jpg")
ball_scale_x = ball_image.get_width() / ball_image.get_height()
ball_scale_y = 1
ball_image = pygame.transform.smoothscale(
    ball_image, (round(img_size_px * ball_scale_x), round(img_size_px * ball_scale_y)))

ball_image_transparent = pygame.Surface((ball_image.get_width(), ball_image.get_height()))
ball_image_transparent.blit(ball_image, (0, 0))
ball_image_transparent.set_alpha(127)


clock = pygame.time.Clock()
santa_sprite_4x4_image = pygame.image.load("./files/img/santa_sprite_4x4.jpg")
pygame.display.set_caption(game_type)


def get_santa_image(i):
    image = pygame.Surface((256, 256))
    x = (i % 4) * 256
    y = (i // 4) * 256
    image.blit(santa_sprite_4x4_image, (0, 0), (x, y, 256, 256))
    return image


images = [i for i in range(16)]
for i in images:
    images[i] = get_santa_image(i)


animation_time_current = 0
animation_time_total = 1.75

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            break
    screen.fill((255, 255, 255))
    screen.blit(text1, (120, 110))
    pygame.display.update()

    sprite_index = math.floor((animation_time_current % 1) * 16)
    x = screen.get_width() / 2 - 128
    y = screen.get_height() / 2 - 128
    image = images[sprite_index]
    screen.blit(image, (x, y))
    pygame.display.flip()
    animation_time_current += clock.tick(target_fps) / 1000
    if animation_time_current >= animation_time_total:
        break

# Игра

SNOWFLAKE = 0
BALL = 1

next_cell_type = SNOWFLAKE
winner = None

cells = {}


def screen_vec_to_game_vec(vec2):
    return (vec2[0] / cell_size_px, vec2[1] / cell_size_px)


def screen_to_game_coords_no_origin(coords):
    return ((coords[0] - screen.get_width() / 2) / cell_size_px,
            (coords[1] - screen.get_height() / 2) / cell_size_px)


def screen_to_game_coords(coords):
    coords = screen_to_game_coords_no_origin(coords)
    return (coords[0] - origin[0],
            coords[1] - origin[1])


def game_to_screen_coords(coords):
    return ((coords[0] + origin[0]) * cell_size_px + screen.get_width() / 2,
            (coords[1] + origin[1]) * cell_size_px + screen.get_height() / 2)


def handle_events():
    global drag_prev
    for event in pygame.event.get():
        handle_event(event)


def handle_event(event):
    global running
    match event.type:
        case pygame.QUIT:
            pygame.quit()
            running = False
        case pygame.MOUSEBUTTONDOWN:
            handle_mouse_button_down()
        case pygame.MOUSEBUTTONUP:
            handle_mouse_button_up()
        case pygame.MOUSEMOTION:
            handle_mouse_motion()


def handle_mouse_button_down():
    global drag_prev
    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        handle_left_mouse_button_down()
    if pressed[1]:
        handle_middle_mouse_button_down()


def handle_left_mouse_button_down():
    global cells, next_cell_type, winner
    cursor_pos = screen_to_game_coords(pygame.mouse.get_pos())
    cursor_pos = (round(cursor_pos[0]), round(cursor_pos[1]))
    if cursor_pos in cells:
        return

    ''' В игре с другим человеком следующий ход передается второму игроку
        В игре с роботом второй ход отдается боту'''
    if game_type == 'человек с человеком':
        cells[cursor_pos] = next_cell_type
        '''проверка выигрыша'''
        if (
            check_line(cursor_pos, (1, 0), next_cell_type)
            or check_line(cursor_pos, (0, 1), next_cell_type)
            or check_line(cursor_pos, (1, 1), next_cell_type)
            or check_line(cursor_pos, (1, -1), next_cell_type)
        ):
            winner = next_cell_type
            next_cell_type = SNOWFLAKE
            return

        next_cell_type = (next_cell_type + 1) % 2

    else:
        cells[cursor_pos] = SNOWFLAKE
        if (
                check_line(cursor_pos, (1, 0), SNOWFLAKE)
                or check_line(cursor_pos, (0, 1), SNOWFLAKE)
                or check_line(cursor_pos, (1, 1), SNOWFLAKE)
                or check_line(cursor_pos, (1, -1), SNOWFLAKE)
        ):
            winner = SNOWFLAKE
            next_cell_type = SNOWFLAKE
            return

        pygame.time.delay(500)

        data = list(cells.keys())
        '''бот выбирает случайную клетку в которой уже есть фишка 
           и ставит в случайную свободную клетку рядом с ней'''

        while True:
            '''проверка на свободные места вокруг клетки'''
            target_cell = random.choice(data)
            target_cells = [(target_cell[0] - 1, target_cell[1] - 1), (target_cell[0], target_cell[1] - 1),
                            (target_cell[0] + 1, target_cell[1] - 1), (target_cell[0] - 1, target_cell[1]),
                            (target_cell[0] + 1, target_cell[1]), (target_cell[0] - 1, target_cell[1] + 1),
                            (target_cell[0], target_cell[1] + 1), (target_cell[0] + 1, target_cell[1] + 1)]
            if any([i not in data for i in target_cells]):
                break

        bot_cell = random.choice(list(filter(lambda x: x not in data, target_cells)))

        cells[bot_cell] = BALL

        '''проверка выигрыша'''
        if (
                check_line(cursor_pos, (1, 0), BALL)
                or check_line(cursor_pos, (0, 1), BALL)
                or check_line(cursor_pos, (1, 1), BALL)
                or check_line(cursor_pos, (1, -1), BALL)
        ):
            winner = BALL
            next_cell_type = BALL
            return


def check_line(pos, direction,cell_type):
    direction2 = (direction[0] * -1, direction[1] * -1)

    return (
        count_cells_in_direction(pos, direction, cell_type)
        + count_cells_in_direction(pos, direction2, cell_type)
        >= 4
    )


def count_cells_in_direction(prev_cell_pos, direction, cell_type):
    cell_pos = (prev_cell_pos[0] + direction[0], prev_cell_pos[1] + direction[1])
    if cell_pos not in cells or cells[cell_pos] != cell_type:
        return 0

    return 1 + count_cells_in_direction(cell_pos, direction, cell_type)


def handle_middle_mouse_button_down():
    global drag_prev
    if drag_prev is not None:
        return
    drag_prev = pygame.mouse.get_pos()


def handle_mouse_button_up():
    pressed = pygame.mouse.get_pressed()
    if not pressed[1]:
        handle_middle_mouse_button_up()


def handle_middle_mouse_button_up():
    global drag_prev
    drag_prev = None


def handle_mouse_motion():
    global drag_prev, origin
    if drag_prev is None:
        return
    pos = pygame.mouse.get_pos()
    offset = screen_vec_to_game_vec((pos[0] - drag_prev[0], pos[1] - drag_prev[1]))
    origin = (origin[0] + offset[0], origin[1] + offset[1])
    drag_prev = pos


def get_mouse_position():
    if not pygame.mouse.get_focused():
        return None
    return pygame.mouse.get_pos()


def render_grid():
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    p0 = screen_to_game_coords((0, 0))
    p0 = (round(p0[0] - 0.5), round(p0[1] - 0.5))
    p1 = screen_to_game_coords((screen_width, screen_height))
    p1 = (round(p1[0] + 0.5), round(p1[1] + 0.5))

    for x in range(p0[0], p1[0] + 1):
        l0 = game_to_screen_coords((x - 0.5, p0[1] - 0.5))
        l1 = game_to_screen_coords((x - 0.5, p1[1] + 0.5))
        pygame.draw.line(screen, grid_color, l0, l1, 2)

    for y in range(p0[1], p1[1] + 1):
        l0 = game_to_screen_coords((p0[0] - 0.5, y - 0.5))
        l1 = game_to_screen_coords((p1[0] + 0.5, y - 0.5))
        pygame.draw.line(screen, grid_color, l0, l1, 2)


def add_winner(winner, game_type):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    winner = ['Снежинки', 'Шары', 'Человек', 'Бот'][winner + 2 if game_type == 'человек с роботом' else winner]
    con = sqlite3.connect("./files/data/wins_story.db")
    cur = con.cursor()
    cur.execute("INSERT INTO story (type, winner, time) VALUES (?, ?, ?)", (game_type, winner, str(current_time)))
    con.commit()
    con.close()


def game_loop():
    running = True

    while running and winner is None:
        handle_events()
        if not running:
            break

        mouse_pos = get_mouse_position()
        cursor_pos = None

        if mouse_pos is not None:
            cursor_pos = screen_to_game_coords(mouse_pos)
            cursor_pos = (round(cursor_pos[0]), round(cursor_pos[1]))

        screen.fill((255, 255, 255))

        for cell_pos in cells:
            cell_type = cells[cell_pos]
            img = snowflake_image
            if cell_type == BALL:
                img = ball_image

            p0 = game_to_screen_coords((cell_pos[0], cell_pos[1]))
            screen.blit(img, (p0[0] - img.get_width() / 2, p0[1] - img.get_height() / 2))

        if (cursor_pos is not None) and (cursor_pos not in cells):
            img = snowflake_image_transparent
            if next_cell_type == BALL:
                img = ball_image_transparent

            p0 = game_to_screen_coords((cursor_pos[0], cursor_pos[1]))
            screen.blit(img, (p0[0] - img.get_width() / 2, p0[1] - img.get_height() / 2))

        render_grid()
        pygame.display.flip()
        clock.tick(target_fps)


def snowflakes_won_text(type):
    global font0
    if type == "человек с человеком":
        return font0.render("Снежинки победили", True, (0, 63, 189))
    return font0.render("Вы победили", True, (0, 63, 189))


def balls_won_text(type):
    global font1
    if type == "человек с человеком":
        return font0.render("Шары победили", True, (0, 63, 189))
    return font0.render("Бот победил", True, (0, 63, 189))


'''Шрифты берутся из отдельных файлов'''

font0 = pygame.font.Font("./files/fonts/Roboto-Regular.ttf", 56)
font1 = pygame.font.Font("./files/fonts/Roboto-Regular.ttf", 24)

click_to_restart_text = font1.render( "Кликните, чтобы начать заново", True, (0, 63, 189))
text_gap = 16
all_text_height = (snowflakes_won_text(game_type).get_height() + text_gap + click_to_restart_text.get_height())


def win_screen():
    global running, winner, origin
    while running and winner is not None:
        for event in pygame.event.get():
            '''Обработчик событий на выход из игры или в меню'''
            if event.type == pygame.QUIT:
                add_winner(winner, game_type)
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                add_winner(winner, game_type)
                winner = None
                origin = (0, 0)
                cells.clear()


        screen.fill((255, 255, 255))

        if winner == BALL:
            win_text = balls_won_text(game_type)
        else:
            win_text = snowflakes_won_text(game_type)

        text_x = (screen.get_width() - win_text.get_width()) / 2
        text_y = (screen.get_height() - all_text_height) / 2
        screen.blit(win_text, (text_x, text_y))

        text_y += win_text.get_height() + text_gap
        text_x = (screen.get_width() - click_to_restart_text.get_width()) / 2
        screen.blit(click_to_restart_text, (text_x, text_y))

        pygame.display.flip()
        clock.tick(target_fps)


if __name__ == '__main__':
    '''Программа бесконечная
       При победе отображается информация о победителе
       Далее можно начать еще одну партию'''
    while running:
        game_loop()
        win_screen()
