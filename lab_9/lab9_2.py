import pygame
import random
import sys
import time

pygame.init()


SCREEN_WIDTH = 800       # Game window width
SCREEN_HEIGHT = 600      # Game window height
CELL_SIZE = 20           # Size of each grid cell

# Color definitions (RGB)
WHITE = (255, 255, 255)  # Background
GREEN = (0, 255, 0)      # Snake
BLACK = (0, 0, 0)        # Text
RED = (255, 0, 0)        # Food type 1
BLUE = (0, 0, 255)       # Food type 2
PURPLE = (160, 32, 240)  # Food type 3

# Game settings
START_SPEED = 10         # Initial game speed
LEVEL_UP_FOOD = 3        # Food needed to level up

# Initialize game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.Font(None, 30)  # Default font


class Snake:
    def __init__(self):
        # Initial snake body
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"  # Starting dircetion
        self.grow = False
    
    def move(self):
        x, y = self.body[0]  # Get head position
        
        # Calculate new head position
        if self.direction == "UP":
            y -= CELL_SIZE
        elif self.direction == "DOWN":
            y += CELL_SIZE
        elif self.direction == "LEFT":
            x -= CELL_SIZE
        elif self.direction == "RIGHT":
            x += CELL_SIZE
        
        new_head = (x, y)
        
        # Wall collision check
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return False  # Game over
        
        # Self collision check
        if new_head in self.body:
            return False
        
        # Movement
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False  # Reset growth flag
        
        return True  # Move successful
    
    def change_direction(self, new_direction):
        opposite_directions = { # Prevents going backwards
            "UP": "DOWN", 
            "DOWN": "UP", 
            "LEFT": "RIGHT", 
            "RIGHT": "LEFT"
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction
    
    def grow_snake(self):
        self.grow = True
    
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, 
                           (segment[0], segment[1], CELL_SIZE, CELL_SIZE))


class Food:
    def __init__(self, snake_body):
        self.position = self.generate_food_position(snake_body)
        self.weight = random.choice([1, 2, 3])  # Random food value
        self.spawn_time = time.time() # Track spawn time
    
    def generate_food_position(self, snake_body):
        while True:
            x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in snake_body:  # Make sure that food will not spawn in snake
                return (x, y)
    
    def should_disappear(self):
        return time.time() - self.spawn_time > 5
    
    def draw(self):
        color = RED
        if self.weight == 2:
            color = BLUE
        elif self.weight == 3:
            color = PURPLE
        pygame.draw.rect(screen, color,(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))


def start_game():
    snake = Snake()
    food = Food(snake.body)
    clock = pygame.time.Clock()
    speed = START_SPEED
    score = 0
    level = 1

    while True:  # Main game loop
        screen.fill(WHITE)  # Clear screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Direction control
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
        
       
        # Move snake
        if not snake.move():
            break  # End game
        
        # Food collision check
        if snake.body[0] == food.position:
            snake.grow_snake()
            score += food.weight  # Add food's weight to score
            food = Food(snake.body)  # Create new food
            
            # Level up every LEVEL_UP_FOOD points
            if score % LEVEL_UP_FOOD == 0:
                level += 1
                speed += 2  # Increase difficulty
        
        # Food expiration check
        if food.should_disappear():
            food = Food(snake.body)  # Replace expired food
        
       
        snake.draw()
        food.draw()
        
        # Display score and level
        score_text = font.render(f"Score: {score}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (SCREEN_WIDTH - 100, 10))
        
        pygame.display.flip()  # Update display
        clock.tick(speed)      # Control game speed
    
    # Game over message
    print(f"Game Over! Final Score: {score}, Level: {level}")


while True:  # Title screen loop
    screen.fill(WHITE)
    start_text = font.render("Press ENTER to Start", True, BLACK)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Start game on Enter
                start_game() 