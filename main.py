import time

import pygame
from fighter import Fighter

pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sasi")

# Установка кадров
clock = pygame.time.Clock()
FPS = 60

# обозначение цветов
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# определяем игровые переменные
intro_count = 3
last_count_update = pygame.time.get_ticks()
fight_text = "FIGHT"

# определяем переменные бойцов
WARRIOR_SIZE = 162
WARRIOR_SCALE = 3
WARRIOR_OFFSET = [66, 45]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 200
WIZARD_SCALE = 3
WIZARD_OFFSET = [80, 70]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# загрузка заднего фона
bg_image = pygame.image.load("assets/images/background/background.png").convert_alpha()

# загрузка анимации
warrior_sheet = pygame.image.load("assets/images/warrior/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizzard/wizzard.png").convert_alpha()

# обозначаем номер анимации
WARRIOR_ANIMATION_STEPS = [10, 8, 3, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]

# Обозначаем шрифт
count_font = pygame.font.Font("assets/fonts/font.ttf", 80)
score_font = pygame.font.Font("assets/fonts/font.ttf", 30)


# функция для отрисовки текста
def draw_text(text1, font, text_col, x, y):
    img = font.render(text1, True, text_col)
    screen.blit(img, (x, y))


# функция для прорисовки заднего фона
def draw_bg():
    scale_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scale_bg, (0, 0))


# функция для отрисовки здоровья бойцов

def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# Создание двух экземпляров класса Fighter

fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

# game loop
run = True
while run:

    clock.tick(FPS)

    # прорисовка фона
    draw_bg()

    # отрисовка здоровья
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    # обновление счётчика
    if intro_count <= 0:
        # движение бойцов
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
    else:
        # отображение таймера
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
        if (pygame.time.get_ticks() - 3000) >= 0:
            draw_text(fight_text, count_font, RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 3)

    # обновление анимации
    fighter_1.update()
    fighter_2.update()

    # прорисовка бойцов
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # обновление экрана
    pygame.display.update()

# exit pygame
pygame.quit()
