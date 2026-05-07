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



