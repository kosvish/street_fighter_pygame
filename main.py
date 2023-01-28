import pygame
from fighter import Fighter

pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sasi")

# загрузка заднего фона
bg_image = pygame.image.load("assets/images/background/background.png").convert_alpha()


# функция для прорисовки заднего фона
def draw_bg():
    scale_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scale_bg, (0, 0))


# Создание двух экземпляров класса Fighter

fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)

# game loop
run = True
while run:

    # прорисовка фона
    draw_bg()

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
