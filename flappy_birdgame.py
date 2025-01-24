import pygame
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 223, 0)

FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_SPEED = 4
PIPE_GAP = 150
HORIZONTAL_SPEED = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird with Coins")

FONT = pygame.font.SysFont("Arial", 30)

bird_width, bird_height = 30, 30
bird_x = 100
bird_y = SCREEN_HEIGHT // 2
bird_velocity_y = 0
bird_velocity_x = 0

pipe_width = 60
pipes = []
pipe_timer = 0

coins = []
coin_radius = 10

score = 0
coin_score = 0

clock = pygame.time.Clock()

running = True
game_over = False

while running:
    screen.fill(BLUE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity_y = JUMP_STRENGTH
            if event.key == pygame.K_r and game_over:
                bird_x = 100
                bird_y = SCREEN_HEIGHT // 2
                bird_velocity_y = 0
                bird_velocity_x = 0
                pipes = []
                coins = []
                score = 0
                coin_score = 0
                game_over = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                bird_velocity_x = -HORIZONTAL_SPEED
            if event.key == pygame.K_d:
                bird_velocity_x = HORIZONTAL_SPEED
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d]:
                bird_velocity_x = 0

    if not game_over:
        bird_velocity_y += GRAVITY
        bird_y += bird_velocity_y
        bird_x += bird_velocity_x
        bird_x = max(0, min(SCREEN_WIDTH - bird_width, bird_x))

    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    pygame.draw.rect(screen, RED, bird_rect)

    if not game_over:
        pipe_timer += 1
        if pipe_timer > 90:
            pipe_timer = 0
            pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
            pipes.append((SCREEN_WIDTH, pipe_height))
            coin_x = SCREEN_WIDTH + pipe_width // 2
            coin_y = pipe_height + PIPE_GAP // 2
            coins.append((coin_x, coin_y))

    new_pipes = []
    for pipe_x, pipe_height in pipes:
        pipe_x -= PIPE_SPEED
        if pipe_x + pipe_width > 0:
            new_pipes.append((pipe_x, pipe_height))

        top_pipe_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        pygame.draw.rect(screen, GREEN, top_pipe_rect)

        bottom_pipe_rect = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, pipe_width, SCREEN_HEIGHT - pipe_height - PIPE_GAP)
        pygame.draw.rect(screen, GREEN, bottom_pipe_rect)

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            game_over = True

        if pipe_x + pipe_width < bird_x and pipe_x + pipe_width + PIPE_SPEED >= bird_x:
            score += 1

    pipes = new_pipes

    new_coins = []
    for coin_x, coin_y in coins:
        coin_x -= PIPE_SPEED
        if coin_x + coin_radius > 0:
            coin_rect = pygame.Rect(coin_x - coin_radius, coin_y - coin_radius, coin_radius * 2, coin_radius * 2)
            if bird_rect.colliderect(coin_rect):
                coin_score += 2
            else:
                new_coins.append((coin_x, coin_y))
            pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), coin_radius)

    coins = new_coins

    if bird_y > SCREEN_HEIGHT or bird_y < 0:
        game_over = True

    score_text = FONT.render(f"Score: {score}", True, BLACK)
    coin_score_text = FONT.render(f"Coins: {coin_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(coin_score_text, (10, 40))

    if game_over:
        game_over_text = FONT.render("Game Over! Press R to Restart", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()