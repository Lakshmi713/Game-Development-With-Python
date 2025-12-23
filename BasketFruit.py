import pygame
import random
import sys

pygame.init()

# Window
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basket and Fruits Game")

# Colors
BG_COLOR = (135, 206, 250)   # sky blue
TEXT_COLOR = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Basket
BASKET_W, BASKET_H = 100, 50
basket_img = pygame.image.load("basket.jfif")
basket_img = pygame.transform.scale(basket_img, (BASKET_W, BASKET_H))
basket_x = WIDTH // 2 - BASKET_W // 2
basket_y = HEIGHT - BASKET_H - 10
basket_rect = pygame.Rect(basket_x, basket_y, BASKET_W, BASKET_H)
basket_speed = 8

# Fruits
FRUIT_W, FRUIT_H = 30, 30
fruit_images = [
    pygame.transform.scale(pygame.image.load("apple.jfif"), (FRUIT_W, FRUIT_H)),
    pygame.transform.scale(pygame.image.load("orange.jfif"), (FRUIT_W, FRUIT_H)),
    pygame.transform.scale(pygame.image.load("pomegranate.jfif"), (FRUIT_W, FRUIT_H))
]

fruits = []
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1000)  # spawn every 1 sec

# Game variables
score = 0
lives = 3
game_over = False
font = pygame.font.SysFont(None, 40)

def reset_game():
    global fruits, score, lives, game_over, basket_rect
    fruits.clear()
    score = 0
    lives = 3
    game_over = False
    basket_rect.x = WIDTH // 2 - BASKET_W // 2

# Game loop
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_EVENT and not game_over:
            x = random.randint(0, WIDTH - FRUIT_W)
            fruit_img = random.choice(fruit_images)
            fruit_rect = pygame.Rect(x, -FRUIT_H, FRUIT_W, FRUIT_H)
            fruits.append({"rect": fruit_rect, "img": fruit_img})
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and basket_rect.x > 0:
            basket_rect.x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_rect.x < WIDTH - BASKET_W:
            basket_rect.x += basket_speed

    # Move fruits
    if not game_over:
        for fruit in fruits:
            fruit["rect"].y += 5

    # Check catch / miss
    for fruit in fruits[:]:
        if basket_rect.colliderect(fruit["rect"]):
            score += 1
            fruits.remove(fruit)
        elif fruit["rect"].y > HEIGHT:
            lives -= 1
            fruits.remove(fruit)
            if lives <= 0:
                game_over = True

    # Draw basket
    screen.blit(basket_img, (basket_rect.x, basket_rect.y))

    # Draw fruits
    for fruit in fruits:
        screen.blit(fruit["img"], (fruit["rect"].x, fruit["rect"].y))

    # Draw score & lives
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))

    # Game Over
    if game_over:
        over_text = font.render("GAME OVER! Press R to Restart", True, (255, 0, 0))
        screen.blit(over_text, (50, HEIGHT//2 - 20))

    pygame.display.flip()
    clock.tick(FPS)
