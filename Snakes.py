import pygame
import sys
import random
import time
import datetime

# Define some constants for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)

# Initialize Pygame
check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized!")

# Game constants
WIDTH, HEIGHT = 720, 460
GRID_SIZE = 10
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Initialize Pygame colors
brown = pygame.Color(165, 42, 42)

# Initialize the start time
start_time = datetime.datetime.now()

# Game variables
fps = 13
fpsClock = pygame.time.Clock()

playSurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game! by Dineth-H® using Python and Pygame')

snakePos = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]

foodPos = [random.randrange(1, GRID_WIDTH) * GRID_SIZE, random.randrange(1, GRID_HEIGHT) * GRID_SIZE]
foodSpawn = True

direction = 'RIGHT'
changeto = direction

score = 0
start_time = datetime.datetime.now()

def game_restart():
    global snakePos, snakeBody, foodPos, foodSpawn, direction, changeto, score, start_time

    # Reset game variables
    snakePos = [100, 50]
    snakeBody = [[100, 50], [90, 50], [80, 50]]
    foodPos = [random.randrange(1, GRID_WIDTH) * GRID_SIZE, random.randrange(1, GRID_HEIGHT) * GRID_SIZE]
    foodSpawn = True
    direction = 'RIGHT'
    changeto = direction
    score = 0
    start_time = datetime.datetime.now()
    
def save_score(username):
    with open("high_scores.txt", "a") as file:
        file.write(f"{username}: {score}\n")

def get_high_score():
    try:
        with open("high_scores.txt", "r") as file:
            lines = file.readlines()
            if lines:
                high_scores = [line.split(":") for line in lines]
                high_scores = {name.strip(): int(score) for name, score in high_scores}
                return max(high_scores, key=high_scores.get), max(high_scores.values())
    except FileNotFoundError:
        return None, 0

def game_over():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render("Game over! Press [R]", True, RED)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (WIDTH // 2, HEIGHT // 4)
    playSurface.blit(GOsurf, GOrect)
    showScore()
    pygame.display.flip()
    time.sleep(2)  # Display game over message for 2 seconds
    wait_for_restart()

def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_restart()
                    return  # Return to the game loop

def showScore():
    sFont = pygame.font.SysFont('monaco', 24)
    Ssurf = sFont.render('Score: {0}'.format(score), True, BLACK)
    Srect = Ssurf.get_rect()
    Srect.midtop = (WIDTH // 10, 10)
    
    # Calculate the elapsed time
    elapsed_time = datetime.datetime.now() - start_time
    elapsed_time_str = f'Time: {elapsed_time.seconds} s'
    
    # Create a text surface for the time
    time_surf = sFont.render(elapsed_time_str, True, BLACK)
    time_rect = time_surf.get_rect()
    
    # Position the time text next to the score
    time_rect.topleft = (WIDTH // 18, 28)
    
    # Draw both score and time on the playSurface
    playSurface.blit(Ssurf, Srect)
    playSurface.blit(time_surf, time_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeto = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeto = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.key == pygame.K_r:
                game_restart()
            if event.key == pygame.K_p:
                username = input("Enter your name: ")
                save_score(username)

    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    if direction == 'RIGHT':
        snakePos[0] += GRID_SIZE
    if direction == 'LEFT':
        snakePos[0] -= GRID_SIZE
    if direction == 'UP':
        snakePos[1] -= GRID_SIZE
    if direction == 'DOWN':
        snakePos[1] += GRID_SIZE

    snakeBody.insert(0, list(snakePos))

    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    if foodSpawn == False:
        foodPos = [random.randrange(1, GRID_WIDTH) * GRID_SIZE, random.randrange(1, GRID_HEIGHT) * GRID_SIZE]
    foodSpawn = True

    # Draw a black boundary around the game window
    pygame.draw.rect(playSurface, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT), 2)  # 2 is the border width
    playSurface.fill(WHITE)

    # Generate random food color
    food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Draw the food with the random color
    pygame.draw.rect(playSurface, food_color, pygame.Rect(foodPos[0], foodPos[1], GRID_SIZE, GRID_SIZE))

    for pos in snakeBody:
    # Draw the green snake segment
        pygame.draw.rect(playSurface, GREEN, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))

    # Draw a black border around the segment
        pygame.draw.rect(playSurface, BLACK, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE), 1)  # 1 is the border width


    if snakePos[0] >= WIDTH or snakePos[0] < 0 or snakePos[1] >= HEIGHT or snakePos[1] < 0:
        game_over()

    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            game_over()

    # Display the high score on the screen
    high_score_name, high_score = get_high_score()
    high_score_text = f'High Score: {high_score_name} - {high_score}'
    highFont = pygame.font.SysFont('monaco', 24)
    high_surf = highFont.render(high_score_text, True, BLACK)
    high_rect = high_surf.get_rect()
    high_rect.midtop = (WIDTH // 2, 10)
    playSurface.blit(high_surf, high_rect)

    showScore()
    pygame.display.flip()
    fpsClock.tick(fps)
