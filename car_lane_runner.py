import pygame
import random
import sys

pygame.init()

# Window
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Lane Runner")

# Colors
ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Lanes
LANE_COUNT = 3
LANE_WIDTH = WIDTH // LANE_COUNT
LANES = [LANE_WIDTH//2 - 25 + i*LANE_WIDTH for i in range(LANE_COUNT)]

# Load images
player_img = pygame.image.load("car.jfif")
player_img = pygame.transform.scale(player_img, (50, 100))

obstacle_img = pygame.image.load("obstaclecar.jfif")
obstacle_img = pygame.transform.scale(obstacle_img, (50, 100))

# Player car
PLAYER_W, PLAYER_H = 50, 100
player_rect = pygame.Rect(LANES[1], HEIGHT - PLAYER_H - 20, PLAYER_W, PLAYER_H)

# Obstacles
OBSTACLE_W, OBSTACLE_H = 50, 100
obstacles = []
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500)

# Game variables
score = 0
game_over = False
font = pygame.font.SysFont(None, 40)

def reset_game():
    global player_rect, obstacles, score, game_over
    player_rect.x = LANES[1]
    player_rect.y = HEIGHT - PLAYER_H - 20
    obstacles.clear()
    score = 0
    game_over = False

# Draw road and lane lines
def draw_road():
    screen.fill((30, 150, 30))  # grass
    pygame.draw.rect(screen, ROAD_COLOR, (0, 0, WIDTH, HEIGHT))
    for i in range(1, LANE_COUNT):
        pygame.draw.line(screen, LINE_COLOR, (i*LANE_WIDTH, 0), (i*LANE_WIDTH, HEIGHT), 4)

# To track key presses (one move per press)
move_left_pressed = False
move_right_pressed = False

# Game loop
running = True
while running:
    draw_road()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_EVENT and not game_over:
            lane = random.choice(LANES)
            rect = pygame.Rect(lane, -OBSTACLE_H, OBSTACLE_W, OBSTACLE_H)
            obstacles.append(rect)
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT:
                    move_left_pressed = True
                if event.key == pygame.K_RIGHT:
                    move_right_pressed = True
            if game_over and event.key == pygame.K_r:
                reset_game()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left_pressed = False
            if event.key == pygame.K_RIGHT:
                move_right_pressed = False

    # Move player one lane per key press
    if move_left_pressed and not game_over:
        idx = LANES.index(player_rect.x)
        if idx > 0:
            player_rect.x = LANES[idx-1]
        move_left_pressed = False  # reset to allow single move per press

    if move_right_pressed and not game_over:
        idx = LANES.index(player_rect.x)
        if idx < len(LANES)-1:
            player_rect.x = LANES[idx+1]
        move_right_pressed = False  # reset to allow single move per press

    # Move obstacles
    if not game_over:
        for obs in obstacles:
            obs.y += 5
        obstacles = [o for o in obstacles if o.y < HEIGHT]
        score += 1 / FPS

    # Draw player
    screen.blit(player_img, (player_rect.x, player_rect.y))

    # Draw obstacles
    for obs in obstacles:
        screen.blit(obstacle_img, (obs.x, obs.y))

    # Collision
    for obs in obstacles:
        if player_rect.colliderect(obs):
            game_over = True

    # Score
    score_text = font.render(f"Score: {int(score)}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

    # Game over
    if game_over:
        over_text = font.render("GAME OVER! Press R to Restart", True, (255, 255, 0))
        screen.blit(over_text, (20, HEIGHT//2 - 20))

    pygame.display.flip()
    clock.tick(FPS)
