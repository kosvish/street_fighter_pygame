import pygame


class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))

    def move(self):
        SPEED = 10
        dx = 0
        dy = 0

        # получаем нажатие клавиш
        key = pygame.key.get_pressed()

        # движение
        if key[pygame.K_a]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = SPEED

        # обновление положения бойца на экране
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
