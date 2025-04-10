import pygame
import math


pygame.init()

# Screen
screen_width = 800
screen_height = 600


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Paint with Pygame")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Default drawing color
drawing_color = WHITE

# Tool modes
MODE_PEN = "pen"
MODE_RECTANGLE = "rectangle"
MODE_CIRCLE = "circle"
MODE_ERASER = "eraser"
MODE_SQUARE = "square"
MODE_RIGHT_TRIANGLE = "right_triangle"
MODE_EQUILATERAL_TRIANGLE = "equilateral_triangle"
MODE_RHOMBUS = "rhombus"

# Current tool mode
current_mode = MODE_PEN

# Variables for drawing shapes
start_pos = None
drawing = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_mode == MODE_PEN or current_mode == MODE_ERASER:
                drawing = True
            elif current_mode in [MODE_RECTANGLE, MODE_CIRCLE, MODE_SQUARE, MODE_RIGHT_TRIANGLE, MODE_EQUILATERAL_TRIANGLE, MODE_RHOMBUS]:
                start_pos = event.pos
                drawing = True

        if event.type == pygame.MOUSEBUTTONUP:
            if current_mode == MODE_RECTANGLE:
                end_pos = event.pos # x2, y2
                #when - -
                if end_pos[0] - start_pos[0] < 0 and end_pos[1] - start_pos[1] < 0:
                    pygame.draw.rect(screen, drawing_color, (end_pos, (abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))), 2)
                #when + +
                if end_pos[0] - start_pos[0] > 0 and end_pos[1] - start_pos[1] > 0:
                    pygame.draw.rect(screen, drawing_color, (start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])), 2)
                #when + -
                if end_pos[0] - start_pos[0] > 0 and end_pos[1] - start_pos[1] < 0:
                    pygame.draw.rect(screen, drawing_color, ((start_pos[0], end_pos[1]), (end_pos[0] - start_pos[0], abs(end_pos[1] - start_pos[1]))), 2)
                #when - +
                if end_pos[0] - start_pos[0] < 0 and end_pos[1] - start_pos[1] > 0:
                    pygame.draw.rect(screen, drawing_color, ((end_pos[0], start_pos[1]), (abs(end_pos[0] - start_pos[0]), end_pos[1] - start_pos[1])), 2)
            elif current_mode == MODE_CIRCLE:
                end_pos = event.pos
                radius = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                pygame.draw.circle(screen, drawing_color, start_pos, radius, 2)
            elif current_mode == MODE_SQUARE:
                end_pos = event.pos
                size = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))  # Ensure square shape
                pygame.draw.rect(screen, drawing_color, (start_pos[0], start_pos[1], size, size), 2)
            elif current_mode == MODE_RIGHT_TRIANGLE:
                end_pos = event.pos
                points = [start_pos, (end_pos[0], start_pos[1]), (start_pos[0], end_pos[1])]
                pygame.draw.polygon(screen, drawing_color, points, 2)
            elif current_mode == MODE_EQUILATERAL_TRIANGLE:
                end_pos = event.pos
                # Calculate the height of an equilateral triangle
                height = abs(end_pos[1] - start_pos[1]) * (3 ** 0.5) / 2
                points = [start_pos, (end_pos[0], end_pos[1]), (start_pos[0] + (end_pos[0] - start_pos[0]) / 2, start_pos[1] - height)]
                pygame.draw.polygon(screen, drawing_color, points, 2)
            elif current_mode == MODE_RHOMBUS:
                end_pos = event.pos
                # Calculate the points for the rhombus
                mid_x = (start_pos[0] + end_pos[0]) / 2
                mid_y = (start_pos[1] + end_pos[1]) / 2
                width = abs(end_pos[0] - start_pos[0])
                height = abs(end_pos[1] - start_pos[1])
                points = [
                    (mid_x, start_pos[1]),  # Top point
                    (end_pos[0], mid_y),    # Right point
                    (mid_x, end_pos[1]),    # Bottom point
                    (start_pos[0], mid_y)  # Left point
                ]
                pygame.draw.polygon(screen, drawing_color, points, 2)

            drawing = False
            start_pos = None

        if event.type == pygame.MOUSEMOTION and drawing:
            if current_mode == MODE_PEN:
                pos = event.pos
                pygame.draw.circle(screen, drawing_color, pos, 5)
            elif current_mode == MODE_ERASER:
                pos = event.pos
                pygame.draw.circle(screen, BLACK, pos, 10)

        # Controls for changing tools and colors
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Pen tool
                current_mode = MODE_PEN
            elif event.key == pygame.K_r:  # Rectangle tool
                current_mode = MODE_RECTANGLE
            elif event.key == pygame.K_c:  # Circle tool
                current_mode = MODE_CIRCLE
            elif event.key == pygame.K_e:  # Eraser tool
                current_mode = MODE_ERASER
            elif event.key == pygame.K_s:  # Square tool
                current_mode = MODE_SQUARE
            elif event.key == pygame.K_t:  # Right triangle tool
                current_mode = MODE_RIGHT_TRIANGLE
            elif event.key == pygame.K_y:  # Equilateral triangle tool
                current_mode = MODE_EQUILATERAL_TRIANGLE
            elif event.key == pygame.K_h:  # Rhombus tool
                current_mode = MODE_RHOMBUS
            elif event.key == pygame.K_1:  # Select color: Black
                drawing_color = BLACK
            elif event.key == pygame.K_2:  # Select color: Red
                drawing_color = RED
            elif event.key == pygame.K_3:  # Select color: Green
                drawing_color = GREEN
            elif event.key == pygame.K_4:  # Select color: Blue
                drawing_color = BLUE

    # Update the display
    
    pygame.time.Clock().tick(999)
    pygame.display.flip()
pygame.quit()