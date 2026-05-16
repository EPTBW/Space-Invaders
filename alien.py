import pygame, random


class Alien(pygame.sprite.Sprite):
    """
    класс для инопланетян, всего 3 вида
    """
    def __init__(self, alien_type, x, y):
         super().__init__()
         self.type = alien_type
         path = f"Images/alien_{alien_type}.png"
         self.image = pygame.image.load(path)
         self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
         self.rect.x += direction


class MysteryShip(pygame.sprite.Sprite):
    """
    класс для мистического корабля, корабль может появиться
    либо с левого, либо с правого края
    """
    def __init__(self, screen_width):
        super().__init__()
        self.screen_width = screen_width
        self.image = pygame.image.load("Images/Mystery.png")
        x = random.choice([0, self.screen_width - self.image.get_width()])
        if x == 0:
            self.speed = 3
        else:
            self.speed = -3
        self.rect = self.image.get_rect(topleft=(x, 15))

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.screen_width:
            self.kill()
        if self.rect.left < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    """
    Класс для бонусов
    """

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill((50, 255, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 800:
            self.kill()


class Boss(pygame.sprite.Sprite):
    """
    Класс для босса 5-ой стадии.
    """

    def __init__(self, screen_width):
        super().__init__()
        # Временная заглушка для босса (фиолетовый прямоугольник)
        self.image = pygame.Surface((120, 80))
        self.image.fill((150, 0, 200))
        self.rect = self.image.get_rect(center=(screen_width / 2, 80))
        self.screen_width = screen_width

        self.health = 30  # Шкала здоровья (30 попаданий)
        self.max_health = 30
        self.speed = 4
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        # Отталкиваемся от краев экрана
        if self.rect.right >= self.screen_width or self.rect.left <= 0:
            self.direction *= -1

    def draw_health(self, surface):
        # Отрисовка шкалы здоровья над боссом
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 15, self.rect.width, 10))
        pygame.draw.rect(surface, (0, 255, 0),
                         (self.rect.x, self.rect.y - 15, self.rect.width * (self.health / self.max_health), 10))

