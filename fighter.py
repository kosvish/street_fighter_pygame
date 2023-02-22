import pygame


class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0: Стоит,  1:бежит, 2:прыгает, 3:атака1, 4:атака2, 5:получение удара, 6: смерть
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        # достаём изображение из листа анимации
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(
                    temp_img, (self.size * self.image_scale, self.size * self.image_scale
                               )))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # получаем нажатие клавиш
        key = pygame.key.get_pressed()
        # может выполнять другие действия, только если в данный момент не атакует
        if not self.attacking:
            # проверка на игрока 1
            if self.player == 1:
                # движение
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True

                # прыжок
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # атаки
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface, target)
                    # определяем какая атака была использована
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2
                        # проверка на игрока 1
                        if self.player == 1:
                            # движение
                            if key[pygame.K_a]:
                                dx = -SPEED
                                self.running = True
                            if key[pygame.K_d]:
                                dx = SPEED
                                self.running = True

                            # прыжок
                            if key[pygame.K_w] and self.jump == False:
                                self.vel_y = -30
                                self.jump = True
                            # атаки
                            if key[pygame.K_r] or key[pygame.K_t]:
                                self.attack(surface, target)
                                # определяем какая атака была использована
                                if key[pygame.K_r]:
                                    self.attack_type = 1
                                if key[pygame.K_t]:
                                    self.attack_type = 2
            # проверка на игрока 2
            if self.player == 2:
                # движение
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True

                # прыжок
                if key[pygame.K_UP] and self.jump is False:
                    self.vel_y = -30
                    self.jump = True
                # атаки
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface, target)
                    # определяем какая атака была использована
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

        # добавление гравитации
        self.vel_y += GRAVITY
        dy += self.vel_y

        # проверка на то что пользователь находится на экране
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # убедимся что бойцы смотрят друг на друга

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # добавление кулдауна на атаку:
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # обновление положения бойца на экране
        self.rect.x += dx
        self.rect.y += dy

    # обновление анимации
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit is True:
            self.update_action(5)  # 5: Hit
        # проверка какое действие выполняет игрок
        elif self.attacking is True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)

        elif self.jump is True:
            self.update_action(2)  # 2: Прыжок
        elif self.running:
            self.update_action(1)  # 1: Бежит
        else:
            self.update_action(0)  # 0: Стоит

        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        # проверка прошло ли время с момента последнего обновления кадра
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # проверка на то что анимация закончилась
        if self.frame_index >= len(self.animation_list[self.action]):
            # если боец умер , окончание анимации
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # проверка на то что атака закончилась
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width,
                self.rect.height
            )
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        # проверка если новое действие отличается от предыдущего
        if new_action != self.action:
            self.action = new_action
            # обновление настроек анимации
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (
            self.rect.x - (self.offset[0] * self.image_scale),
            self.rect.y - (self.offset[1] * self.image_scale)))
