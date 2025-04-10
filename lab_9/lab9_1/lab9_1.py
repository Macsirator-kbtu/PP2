import pygame
import random

pygame.init()

# Player's starting position
x = 420  # Horizontal position (center of the road)
y = 550  # Vertical position (near the bottom)

# Screen dimensions
screen_width = 840
screen_height = 650

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car game")  # Window title

# Background image (road)
bg = pygame.image.load("Lab_9/lab9_1/Road.png").convert_alpha()

# Player car image
Player = pygame.image.load("Lab_9/lab9_1/Player_car.png").convert_alpha()

# Enemy car image
Enemy = pygame.image.load("Lab_9/lab9_1/Enemy_car.png").convert_alpha()

# Original coin image
Coin = pygame.image.load("Lab_9/lab9_1/Coin.png").convert_alpha()

coin_width = Coin.get_width() // 10
coin_height = Coin.get_height() // 10
Coin = pygame.transform.scale(Coin, (coin_width, coin_height))  # Apply scaling

bg_y = 0  # Background vertical position
Enemy_y = -100  # Initial Y position for enemy cars

# Timer for enemy car spawning (every 500ms = 0.5 seconds)
spawn_enemy = pygame.USEREVENT + 1  # Custom event ID
pygame.time.set_timer(spawn_enemy, 500)
enemy_list = []  # Stores all active enemy cars

# Timer for coin spawning
spawn_coin = pygame.USEREVENT + 1  # Custom event ID
pygame.time.set_timer(spawn_coin, 1500)
coin_list = []  # Stores coins

a = 1  # Base enemy speed multiplier
b = 0  # Acceleration of enemies speed

# --- Font setup for UI ---
label = pygame.font.Font("Lab_9/lab9_1/Arial.ttf", 60)  # Game over text
lose_label = label.render("You lose", False, (193, 196, 199))  # Gray text
restart_label = label.render("Restart", False, (115, 132, 148))  # Blue-gray text
rect_for_restart = restart_label.get_rect(topleft=(315, 305))  # Position for restart button

font = pygame.font.SysFont("Arial", 30) # Score display
Score = 0  # Player's current score

gameplay = True
running = True  # Main game loop control


while running:
    # Draw scrolling background
    screen.blit(bg, (0, bg_y + 0))  # Primary background
    screen.blit(bg, (0, bg_y - 650))  # Secondary background

    if gameplay:
        # Scroll background downward
        bg_y += 10
        if bg_y >= 650: # Reset when scrolled completely
            bg_y = 0

        # Collision of player
        player_rect = Player.get_rect(topleft=(x, y))

        # Increase difficulty
        if Score != 0 and Score % 4 >= 0:
            b = Score / 4  # Accelaration of enemy

        if enemy_list:
            for (i, el) in enumerate(enemy_list):
                screen.blit(Enemy, el)  # Draw each enemy car
                # Speed of enemy
                el.y += 12 * (a + (b/10))
                
                # Remove enemies that go off-screen
                if el.y > 650:
                    enemy_list.pop(i)
                
                # Check collision with player
                if player_rect.colliderect(el):
                    gameplay = False  # Game over

        if coin_list:
            for (i, el) in enumerate(coin_list):
                screen.blit(Coin, el)  # Draw each coin
                
                # Check if player collected the coin
                if player_rect.colliderect(el):
                    c = random.randrange(1, 3)  # Random points 
                    Score += c  # Add to score
                    coin_list.pop(i)  # Remove collected coin

        # Position for next enemy
        Enemy_x = random.randrange(140, 650) 

        # Position for next coin
        coin_spawn_x = random.randrange(140, 610) 
        coin_spawn_y = random.randrange(0, 605)

        # Collision of coins
        coin_rect = Coin.get_rect(topleft=(coin_spawn_x, coin_spawn_y))

        # Draw player car at current position
        screen.blit(Player, (x, y))

        pressed = pygame.key.get_pressed()  # Get all pressed keys
        
        # Right movement (D or Right Arrow)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            x += 7
            if x > 650:  # Right boundary
                x = 650
                
        # Left movement (A or Left Arrow)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            x -= 7
            if x < 140:  # Left boundary
                x = 140
                
        # Down movement (S or Down Arrow)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            y += 7
            if y > 630:  # Bottom boundary
                y = 630
                
        # Up movement (W or Up Arrow)
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            y -= 4
            if y < 0:  # Top boundary
                y = 0
                
        # Turbo boost (Spacebar)
        if pressed[pygame.K_SPACE]:
            y -= 7
            if y < 0:
                y = 0

    else:
        screen.fill((87, 88, 89))
        
        # Draw "You lose" text
        screen.blit(lose_label, (300, 205))
        
        # Draw restart button
        screen.blit(restart_label, rect_for_restart)

        # Check if restart button is clicked
        mouse = pygame.mouse.get_pos()
        if rect_for_restart.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            # Reset
            gameplay = True
            x = 420 
            y = 550 
            Score = 0  # Reset score
            b = 0  # Reset difficulty
            enemy_list.clear()
            coin_list.clear()

    # Render and display score
    score_text = font.render(f"Score: {Score}", False, "Black")
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 60))

    # Update display
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Window close button
            running = False
            
        # Spawn new enemy cars
        if event.type == spawn_enemy:
            for _ in range(6):
                enemy_list.append(Enemy.get_rect(topleft=(Enemy_x, Enemy_y)))
                
        # Spawn new coins
        if event.type == spawn_coin:
            coin_list.append(Coin.get_rect(topleft=(coin_spawn_x, coin_spawn_y)))

    # Cap the game at 60 FPS
    pygame.time.Clock().tick(60)
    pygame.display.flip()  # Final display update