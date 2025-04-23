import pygame
import random
import json
import os
from user import get_or_create_user, get_user_score, save_score

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
INFO_HEIGHT = 40
SAVE_FILE = "GameState.json"

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
FOOD_COLORS = {1: (255, 100, 100), 2: (255, 165, 0), 3: (255, 255, 0)}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

wall_patterns = [
    [],
    [(200, 200, 400, GRID_SIZE)],
    [(100, 300, 600, GRID_SIZE), (400, 100, GRID_SIZE, 400)],
    [(100, 100, GRID_SIZE, 400), (600, 100, GRID_SIZE, 400)],
    [(140, 140, 520, GRID_SIZE), (140, 440, 520, GRID_SIZE)],
]

def get_wall_pattern(level):
    return wall_patterns[level % len(wall_patterns)]

def save_game_to_file(username, state):
    data = {}
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    data[username] = state
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game_from_file(username):
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get(username)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def delete_save_for_user(username):
    if not os.path.exists(SAVE_FILE): return
    with open(SAVE_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    data.pop(username, None)
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.Font(None, size)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y) if center else (x, y))
    screen.blit(surf, rect)

def get_username_and_choice():
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    font = pygame.font.Font(None, 32)
    text = ''
    buttons = {
        "New Game": pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 120, 40),
        "Continue": pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + 50, 120, 40)
    }
    while True:
        screen.fill(WHITE)
        draw_text("Enter your username:", 36, BLACK, WIDTH // 2, HEIGHT // 2 - 60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key, btn in buttons.items():
                    if btn.collidepoint(event.pos):
                        return text.strip(), "new" if key == "New Game" else "continue"

        pygame.draw.rect(screen, (200, 200, 200), input_box)
        txt_surface = font.render(text, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, BLACK, input_box, 2)

        for label, rect in buttons.items():
            pygame.draw.rect(screen, (100, 200, 100), rect)
            draw_text(label, 24, BLACK, rect.centerx, rect.centery)

        pygame.display.flip()
        clock.tick(30)

class Food:
    def __init__(self, walls):
        self.walls = walls
        self.generate()

    def generate(self):
        while True:
            self.position = (
                random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                random.randint(INFO_HEIGHT // GRID_SIZE, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            )
            if all(not pygame.Rect(*wall).collidepoint(self.position) for wall in self.walls):
                break
        self.value = random.randint(1, 3)
        self.timer = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(screen, FOOD_COLORS[self.value], (*self.position, GRID_SIZE, GRID_SIZE))

    def expired(self):
        return pygame.time.get_ticks() - self.timer > 7000

def main():
    username, choice = get_username_and_choice()
    user_id = get_or_create_user(username)
    saved_state = load_game_from_file(username) if choice == "continue" else None
    record_score, _, _ = get_user_score(user_id)

    if choice == "new":
        delete_save_for_user(username)
        score, level, speed = 0, 1, 10
    else:
        score, level, speed = 0, 1, 10

    snake = [(100, 100), (80, 100), (60, 100)]
    snake_dir = (GRID_SIZE, 0)
    food_count = 0
    paused = False
    current_wall_pattern = get_wall_pattern(level)
    food = Food(current_wall_pattern)

    if saved_state:
        snake = [tuple(pos) for pos in saved_state['snake']]
        snake_dir = tuple(saved_state['snake_dir'])
        food_count = saved_state['food_count']
        food.position = tuple(saved_state['food_position'])
        food.value = saved_state['food_value']
        current_wall_pattern = saved_state['wall_pattern']
        score = saved_state['score']
        level = saved_state['level']
        speed = saved_state['speed']

    running = True
    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, INFO_HEIGHT))
        draw_text(f"Score: {score}  Level: {level}", 30, WHITE, WIDTH // 2, INFO_HEIGHT // 2)

        for wall in current_wall_pattern:
            pygame.draw.rect(screen, BLACK, wall)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, GRID_SIZE): snake_dir = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -GRID_SIZE): snake_dir = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (GRID_SIZE, 0): snake_dir = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-GRID_SIZE, 0): snake_dir = (GRID_SIZE, 0)
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_s:
                    save_game_to_file(username, {
                        'snake': snake,
                        'snake_dir': snake_dir,
                        'food_count': food_count,
                        'food_position': food.position,
                        'food_value': food.value,
                        'wall_pattern': current_wall_pattern,
                        'score': score,
                        'level': level,
                        'speed': speed
                    })
                    print("Game saved.")

        if paused:
            draw_text("PAUSED", 60, BLACK, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            clock.tick(5)
            continue

        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        if (new_head in snake or new_head[0] < 0 or new_head[1] < INFO_HEIGHT or
                new_head[0] >= WIDTH or new_head[1] >= HEIGHT or
                any(pygame.Rect(*wall).collidepoint(new_head) for wall in current_wall_pattern)):
            break

        snake.insert(0, new_head)
        if new_head == food.position:
            score += food.value
            food_count += 1
            if food_count % 3 == 0:
                level += 1
                speed += 2
                current_wall_pattern = get_wall_pattern(level)
            food.walls = current_wall_pattern
            food.generate()
        else:
            snake.pop()

        if food.expired():
            food.generate()

        food.draw()
        for seg in snake:
            pygame.draw.rect(screen, GREEN, (*seg, GRID_SIZE, GRID_SIZE))
        pygame.display.flip()
        clock.tick(speed)

    screen.fill(BLACK)
    draw_text("Game Over", 50, WHITE, WIDTH // 2, HEIGHT // 2 - 40)
    draw_text(f"Final Score: {score}  Level: {level}", 30, WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text("Press any key to exit", 25, WHITE, WIDTH // 2, HEIGHT // 2 + 40)
    pygame.display.flip()

    if score > record_score:
        save_score(user_id, score, level, speed)

    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                pygame.quit(); exit()

if __name__ == "__main__":
    main()