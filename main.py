import sys, random
from game import Game
import pygame

pygame.init()

#Color
GREY = (29, 29, 27)
YELLOW = (243, 216, 63)
RED = (241, 14, 14)

#Font, text in game
font = pygame.font.Font("Font/monogram.ttf", 50)
level_surface = font.render("Level 1", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, RED)

#Screen ang game window variables
GAME_WIDTH = 800
GAME_HEIGHT = 600

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

#Offset
OFFSET_Y = 10

#Game surface
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
score_text_surface = font.render("SCORE", False, YELLOW)
high_score_text_surface = font.render("HIGH SCORE", False, YELLOW)

#Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

#Clock
clock = pygame.time.Clock()

game = Game(GAME_WIDTH, GAME_HEIGHT, OFFSET_Y)

#UserEvent
SHOOT_LASER = pygame.USEREVENT
MYSTERY_SHIP = pygame.USEREVENT + 1

#Timer
pygame.time.set_timer(SHOOT_LASER,1000)
pygame.time.set_timer(MYSTERY_SHIP,random.randint(8000,10000))

#Offset для корректировки позиции врагов и корабля игрока
game_offset_x = (SCREEN_WIDTH - GAME_WIDTH) // 2
game_offset_y = (SCREEN_HEIGHT - GAME_HEIGHT) // 2

current_level = game.level

#Loop
while True:
    # Динамическое изменение скорости стрельбы при переходе на новый уровень
    if game.level != current_level:
        current_level = game.level
        pygame.time.set_timer(SHOOT_LASER, game.laser_delay)

    # Checking for Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()
        if event.type == MYSTERY_SHIP and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERY_SHIP, random.randint(10000, 20000))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not game.run:
            game.reset()
            current_level = game.level
            pygame.time.set_timer(SHOOT_LASER, game.laser_delay)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                game.aliens_group.empty()
                if game.boss_group.sprite:
                    game.boss_group.sprite.kill()

    # Updating
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()

        # Обновляем новые группы
        game.boss_group.update()
        game.powerup_group.update()

        game.check_collisions()
        game.check_level_completion()  # Проверяем, пройден ли уровень

    # Drawing
    screen.fill(GREY)
    game_surface.fill(GREY)

    game.spaceship_group.draw(game_surface)
    game.spaceship_group.sprite.laser_group.draw(game_surface)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(game_surface)
    game.aliens_group.draw(game_surface)
    game.alien_lasers_group.draw(game_surface)
    game.mystery_ship_group.draw(game_surface)

    # Отрисовка босса и бонусов
    game.powerup_group.draw(game_surface)
    game.boss_group.draw(game_surface)
    if game.boss_group.sprite:
        game.boss_group.sprite.draw_health(game_surface)

    # Итерфейс
    if game.run:
        screen.blit(game_surface, (game_offset_x, game_offset_y))

        # Динамический текст уровня
        level_surface = font.render(f"Level {game.level}", False, YELLOW)
        screen.blit(level_surface, (720, 720, 50, 50))
    else:
        screen.blit(game_over_surface, (720, 720, 50, 50))

    #Жизни корабля
    x = 50
    for lives in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 740))
        x += 50

    #Счет и лучший счет
    screen.blit(score_text_surface, (50,15,50,50))
    screen.blit(high_score_text_surface, (600,15,50,50))

    formated_score = str(game.score).zfill(5)
    score_surface = font.render(formated_score, False, YELLOW)
    screen.blit(score_surface, (160,15,50,50))

    formated_high_score = str(game.high_score).zfill(5)
    high_score_surface = font.render(formated_high_score, False, YELLOW)
    screen.blit(high_score_surface, (800,15,50,50))

    pygame.draw.rect(screen, YELLOW, (game_offset_x - 2, game_offset_y - 2, GAME_WIDTH + 4, GAME_HEIGHT + 4),
                     2,0, 0,
                     0 ,60 , 60)

    pygame.display.update()
    clock.tick(60)

