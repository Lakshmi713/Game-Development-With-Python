import pygame
import random
import sys

pygame.init()

# ---------------- Screen Setup ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Popper")

# ---------------- Colors ----------------
WHITE = (255, 255, 255)
BLUE = (100, 200, 255)
DARK_BLUE = (30, 60, 120)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# ---------------- Game Variables ----------------
clock = pygame.time.Clock()      
FPS = 60

bubble_list = []
bubble_radius = 25
bubble_speed = 3
bubble_spawn_rate = 30  # lower = more bubbles

score = 0
font = pygame.font.SysFont("Arial", 36)

# ---------------- Background Music (Optional) ----------------
# pygame.mixer.music.load("background.mp3")
# pygame.mixer.music.play(-1)

# ---------------- Game Loop ----------------
running = True
while running:
    screen.fill(DARK_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Mouse click to pop
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for bubble in bubble_list[:]:
                bx, by = bubble
                distance = ((bx - mouse_x) ** 2 + (by - mouse_y) ** 2) ** 0.5
                if distance < bubble_radius:
                    bubble_list.remove(bubble)
                    score += 1

    # Spawn bubbles
    if random.randint(1, bubble_spawn_rate) == 1:
        bx = random.randint(bubble_radius, WIDTH - bubble_radius)
        by = HEIGHT + bubble_radius
        bubble_list.append([bx, by])

    # Move bubbles upward
    for bubble in bubble_list[:]:
        bubble[1] -= bubble_speed
        if bubble[1] + bubble_radius < 0:
            bubble_list.remove(bubble)

    # Draw bubbles
    for bx, by in bubble_list:
        pygame.draw.circle(screen, BLUE, (bx, by), bubble_radius)
        pygame.draw.circle(screen, WHITE, (bx, by), bubble_radius, 2)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Game over condition
    if score >= 30:
        win_text = font.render("You Win! Press R to Restart", True, RED)
        screen.blit(win_text, (WIDTH // 2 - 220, HEIGHT // 2))
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    score = 0
                    bubble_list.clear()
                    waiting = False

    pygame.display.update()
    clock.tick(FPS)
