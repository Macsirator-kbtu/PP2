import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movable Red Ball")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
ball_radius = 25
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
move_step = 20 

def draw_ball():
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    pygame.display.flip()

def move_ball(dx, dy):
    global ball_x, ball_y
    
    # Calculate new position
    new_x = ball_x + dx
    new_y = ball_y + dy
    
    # Check boundaries
    if ball_radius <= new_x <= WIDTH - ball_radius:
        ball_x = new_x
    if ball_radius <= new_y <= HEIGHT - ball_radius:
        ball_y = new_y

# Main game loop
running = True
draw_ball()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_ball(-move_step, 0)
            elif event.key == pygame.K_RIGHT:
                move_ball(move_step, 0)
            elif event.key == pygame.K_UP:
                move_ball(0, -move_step)
            elif event.key == pygame.K_DOWN:
                move_ball(0, move_step)
            
            draw_ball()

pygame.quit()
sys.exit()