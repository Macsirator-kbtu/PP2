import pygame

pygame.init()

# Screen settings
screen_width = 1500
screen_height = 750

# Create the screen
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
            elif current_mode == MODE_RECTANGLE or current_mode == MODE_CIRCLE:
                start_pos = event.pos # x1, y1
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
                end_pos = event.pos # x2, y2
                radius = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                pygame.draw.circle(screen, drawing_color, start_pos, radius, 2)
            drawing = False
            start_pos = None

        if event.type == pygame.MOUSEMOTION and drawing:
            if current_mode == MODE_PEN:
                pos = event.pos
                pygame.draw.circle(screen, drawing_color, pos, 5)
            elif current_mode == MODE_ERASER:
                pos = event.pos
                pygame.draw.circle(screen, BLACK, pos, 10)



        # Handle key presses for tool selection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Pen tool
                current_mode = MODE_PEN
            elif event.key == pygame.K_r:  # Rectangle tool
                current_mode = MODE_RECTANGLE
            elif event.key == pygame.K_c:  # Circle tool
                current_mode = MODE_CIRCLE
            elif event.key == pygame.K_e:  # Eraser tool
                current_mode = MODE_ERASER
            elif event.key == pygame.K_1:  # Select color: Black
                drawing_color = BLACK
            elif event.key == pygame.K_2:  # Select color: Red
                drawing_color = RED
            elif event.key == pygame.K_3:  # Select color: Green
                drawing_color = GREEN
            elif event.key == pygame.K_4:  # Select color: Blue
                drawing_color = BLUE
            elif event.key == pygame.K_5:
                drawing_color = WHITE

    # Update the display
    pygame.display.flip()
    

# Quit Pygame
pygame.quit()