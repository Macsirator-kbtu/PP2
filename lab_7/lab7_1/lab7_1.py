import pygame
import math
from datetime import datetime

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
try:
    background = pygame.image.load(r"C:\Users\ivano\PyGames\lab_7\lab7_1\mickey_clock_face.png").convert_alpha()
    right_hand = pygame.image.load(r"C:\Users\ivano\PyGames\lab_7\lab7_1\right_hand.png").convert_alpha()  # minute hand
    left_hand = pygame.image.load(r"C:\Users\ivano\PyGames\lab_7\lab7_1\left_hand.png").convert_alpha()    # second hand
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    print("Error loading images")
    pygame.quit()
    exit()

# Clock center
center = (WIDTH//2, HEIGHT//2)

def rotate_hand(image, angle, pivot):
    # Rotate image while keeping the pivot point fixed
    rotated = pygame.transform.rotate(image, -angle)
    # Adjust position so it rotates around the pivot point
    rect = rotated.get_rect(center=pivot)
    return rotated, rect

def draw_clock():
    current = datetime.now()
    
    #angle calculation
    minute_angle = (current.minute / 60) * 360 + 60
    second_angle = (current.second / 60) * 360 + 90
    
    screen.fill(WHITE)
    screen.blit(background, (0, 0))
    
    # Draw minute hand (right hand)
    right_img, right_pos = rotate_hand(right_hand, minute_angle, center)
    screen.blit(right_img, right_pos)
    
    # Draw second hand (left hand)
    left_img, left_pos = rotate_hand(left_hand, second_angle, center)
    screen.blit(left_img, left_pos)
    
    # Draw center dot
    pygame.draw.circle(screen, BLACK, center, 15)
    
    pygame.display.flip()

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_clock()
    clock.tick(30)

pygame.quit()