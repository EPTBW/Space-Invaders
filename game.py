import pygame, random
from pygame.examples import aliens

from laser import Laser
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from alien import MysteryShip


class Game:
    """
    class that contains all the game objects
    """
    def __init__(self, screen_width, screen_height, offset_y):
        self.offset_y = offset_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(screen_width, screen_height, self.offset_y))
        self.obstacles = self.create_obstacles(offset_y)
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.run = True
        self.score = 0
        self.high_score = 0
        self.explosion_sound = pygame.mixer.Sound("Sound/explosion.ogg")
        self.load_high_score()
        pygame.mixer.music.load("Sound/6 - Skid Kid.mp3")
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play(-1)
        self.explosion_sound.set_volume(0.05)

    def create_obstacles(self, offset_y):
        """
        создаем маелнькие обхекты для баррикад, баррикада состоит
        из множества этих объектов
        """
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width - (4 * obstacle_width)) / 5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100 - self.offset_y)
            obstacles.append(obstacle)
        return obstacles

    def create_aliens(self):
        """
        создаем сетку врагов
        """
        for row in range(5):
            for col in range(11):
                x = 100 + col * 55
                y = 30 + row * 55

                if row == 0:
                    alien_type = 3
                elif row in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x ,y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        """
        функция реализующая движение врагов, как только они достигают
        края экрана они спускаются
        """
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.aliens_direction = 1
                self.alien_move_down(2)

    def  alien_move_down(self, distance):
        """
        спуск вниз
        """
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        """
        враги тоже стреляют лазером, враг который будет стрелять лазером определяется
        через функцию random.choice
        """
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

    def create_mystery_ship(self):
        """
        мистический корабль появляется случайно
        """
        self.mystery_ship_group.add(MysteryShip(self.screen_width))

    def check_collisions(self):
        """
        если спрайт лазера пересекается со спрайтом инопланетянина
        спрайты пересекаются, оба спрайта удалаяются через kill()
        """
        #spaceship laser
        if self.spaceship_group.sprite.laser_group:
            #aliens
            for laser_sprite in self.spaceship_group.sprite.laser_group:

                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.update_high_score()
                        laser_sprite.kill()
                        self.explosion_sound.play()
                #mystery ship
                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.score += 500
                    self.update_high_score()
                    laser_sprite.kill()
                    self.explosion_sound.play()
                #barricade
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        #alien lasers
        if self.alien_lasers_group:
            #spaceship
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    laser_sprite.kill()
                    self.lives -= 1
                    self.check_for_lives()
                    print("spaceship hit")
            #barricade
            for obstacle in self.obstacles:
                pygame.sprite.groupcollide(self.alien_lasers_group, obstacle.blocks_group, True, True)

        #aliens sprite
        if self.aliens_group:
            for alien in self.aliens_group:
                #barricade
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)
                #spaceship
                if  pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()

    def check_for_lives(self):
        """
        проверка на количество жизней, жизней нет - проигрышь
        """
        if self.lives == 0:
            self.game_over()

    def game_over(self):
        """
        флаг для проверки проиграл ли игрок
        """
        self.run = False
        print("GAME OVER")

    def update_high_score(self):
        """
        обновляем лучший счет, создаем файл куда будем его записывать
        """
        if self.score > self.high_score:
            self.high_score = self.score

            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))

    def load_high_score(self):
        """
        читаем лучший счет из файла если он есть
        """
        try:
            with open("high_score.txt", "r") as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0

    def reset(self):
        """
        если мы проиграли, и игрок решил начать заново
        откатываем все назад
        """
        self.run = True
        self.lives = 3
        self.score = 0

        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.mystery_ship_group.empty()

        self.create_aliens()
        self.obstacles = self.create_obstacles(self.offset_y)

