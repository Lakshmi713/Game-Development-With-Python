import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Spawn Directions")

WHITE = (255, 255, 255)
BLUE = (0, 150, 255)

clock = pygame.time.Clock()

bubble_radius = 15
bubble_speed = 3

bubbles = []  # Each bubble = [x, y, dx, dy]

SPAWN_DELAY = 800
last_spawn = pygame.time.get_ticks()

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    current_time = pygame.time.get_ticks()

    # -------- Spawn bubble --------
    if current_time - last_spawn > SPAWN_DELAY:
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            x = random.randint(bubble_radius, WIDTH - bubble_radius)
            y = -bubble_radius
            dx, dy = 0, bubble_speed

        elif side == "bottom":
            x = random.randint(bubble_radius, WIDTH - bubble_radius)
            y = HEIGHT + bubble_radius
            dx, dy = 0, -bubble_speed

        elif side == "left":
            x = -bubble_radius
            y = random.randint(bubble_radius, HEIGHT - bubble_radius)
            dx, dy = bubble_speed, 0

        else:  # right
            x = WIDTH + bubble_radius
            y = random.randint(bubble_radius, HEIGHT - bubble_radius)
            dx, dy = -bubble_speed, 0

        bubbles.append([x, y, dx, dy])
        last_spawn = current_time

    # -------- Move & Draw --------
    for bubble in bubbles[:]:
        bubble[0] += bubble[2]
        bubble[1] += bubble[3]

        pygame.draw.circle(screen, BLUE, (bubble[0], bubble[1]), bubble_radius)

        # Remove bubble if outside screen
        if (bubble[0] < -bubble_radius or bubble[0] > WIDTH + bubble_radius or
            bubble[1] < -bubble_radius or bubble[1] > HEIGHT + bubble_radius):
            bubbles.remove(bubble)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit()
