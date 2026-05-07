import pygame
from laser import Laser


class Spaceship(pygame.sprite.Sprite):
    """
    Spaceship class
    """
    def __init__(self, screen_width, screen_height, offest_y):
        super().__init__()
        self.offest_y = offest_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load('Images/spaceship.png')
        self.rect = self.image.get_rect(midbottom = (self.screen_width/2, self.screen_height - offest_y))
        self.speed = 6
        self.laser_group = pygame.sprite.GroupSingle()
        self.laser_sound = pygame.mixer.Sound('Sound/laser.ogg')
        self.laser_sound.set_volume(0.1)

    def get_user_input(self):
        """
        function that gets user input and do actions
        according to the user input
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:#RIGHT
            if self.rect.x < self.screen_width - self.rect.width:
                self.rect.x += self.speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:#LEFT
            if self.rect.x > 0:
                self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and len(self.laser_group) == 0:
            laser = Laser(self.rect.center, 10 , self.screen_height)
            self.laser_group.add(laser)
            self.laser_sound.play()

    def update(self):
        self.get_user_input()
        self.laser_group.update()

    def reset(self):
        self.rect = self.image.get_rect(midbottom = (self.screen_width/2, self.screen_height - self.offest_y))
        self.laser_group.empty()
