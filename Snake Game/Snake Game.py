"""
Snake Eater
Made with PyGame
"""

import random
import sys
import time
from os import path

import pygame
import pygame_menu

# Music
snd_dir = path.join(path.dirname(__file__), 'snd')
pygame.mixer.init()
pygame.mixer.music.load(path.join(snd_dir, 'FrozenJam_BGMusic.ogg'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)


# Difficulty settings:
# Easy       ->  10
# Medium     ->  25
# Hard       ->  60
# Impossible ->  120
difficulty = 25


# Window size
frame_size_x = 720
frame_size_y = 480

# Background images
img_dir = path.join(path.dirname(__file__), 'img')
bg_game = pygame.image.load(path.join(img_dir, 'bg_game.jpg'))
new_bg = pygame.transform.scale(bg_game, (frame_size_x, frame_size_y))

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Main logic
def start_the_game():
    # Game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

    food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True

    direction = 'RIGHT'
    change_to = direction

    score = 0

    # Game Over
    def game_over():
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        show_score(0, red, 'times', 20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    # Score
    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (frame_size_x / 10, 15)
        else:
            score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
        game_window.blit(score_surface, score_rect)
        # pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
        food_spawn = True

        # GFX
        game_window.blit(new_bg, (0, 0))

        # game_window.fill(black)
        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0:
            snake_pos[0] = frame_size_x
        elif snake_pos[0] > frame_size_x - 10:
            snake_pos[0] = 0
        elif snake_pos[1] < 0:
            snake_pos[1] = frame_size_y
        elif snake_pos[1] > frame_size_y - 10:
            snake_pos[1] = 0

        # if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        #     game_over()
        # if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        #     game_over()

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        show_score(1, white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)


def set_difficulty(value, difficulty):
    pass

menu = pygame_menu.Menu(400, 400, 'Welcome',
                        theme=pygame_menu.themes.THEME_DARK)

menu.add_text_input('Name :', default='John Doe')
menu.add_selector('Difficulty :', [('Hard', 60), ('Easy', 25), ('Impossible', 120)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(game_window)
