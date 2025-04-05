import pygame
import time
import random
from ai_controller import AIController

snake_speed = 10

# Window size
window_x = 480
window_y = 240

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
sky_blue = pygame.Color(135, 206, 250)  # Sky blue background

# pygame ka intialization
pygame.init()

# Initialize pygame mixer for audio
pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load('aniket music.mp3')  # Ensure the file name and extension are correct
pygame.mixer.music.play(-1)  # -1 makes it loop indefinitely

# game window intialize krne ke liye
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# fps control ke liye
fps = pygame.time.Clock()

# snake ka default pos
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True

# setting default snake direction towards right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

# AI control toggle
ai_control = False

# displaying Score function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# game over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)

# Restart function
def restart_game():
    global snake_position, snake_body, fruit_position, score, direction, change_to, fruit_spawn, ai_control, snake_speed
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    ai_control = False
    snake_speed = 15

# Main Function
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_a:  # Toggle AI control with 'A' key
                ai_control = not ai_control
            if event.key == pygame.K_r:  # Restart game with 'R' key
                restart_game()
            if event.key == pygame.K_q:  # Quit game with 'Q' key
                pygame.quit()
                quit()

    # AI control logic
    if ai_control:
        ai = AIController(snake_position, fruit_position, snake_body, window_x, window_y)
        change_to = ai.get_direction()

    # If two keys pressed simultaneously
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
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        snake_speed += 1  # Increase speed
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
        restart_game()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()
        restart_game()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
            restart_game()

    # displaying score continuously
    game_window.fill(sky_blue)  # Set background to sky blue
    for pos in snake_body:
        pygame.draw.rect(game_window, black, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))  # Red fruit

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
