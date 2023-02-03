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

# загрузка заднего фона
bg_image = pygame.image.load("assets/images/background/background.png").convert_alpha()

# загрузка анимации
warrior_sheet = pygame.image.load("assets/images/warrior/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizzard/wizzard.png").convert_alpha()

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

fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)

# game loop
run = True
while run:

    clock.tick(FPS)

    # прорисовка фона
    draw_bg()

    # отрисовка здоровья
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    # движение бойцов
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)

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
