import pygame
import random

pygame.init()

x = 420
y = 550

# How big screen is
screen_width = 840
screen_height = 650


#screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car game")


# Images
bg = pygame.image.load("lab_8/lab8_1/Road.png").convert_alpha()
Player = pygame.image.load("lab_8/lab8_1/Player_car.png").convert_alpha()
Enemy = pygame.image.load("lab_8/lab8_1/Enemy_car.png").convert_alpha()
Coin = pygame.image.load("lab_8/lab8_1/Coin.png").convert_alpha()
Coin = pygame.transform.scale(Coin, (40, 45))



#Fone
bg_y = 0

Enemy_y = -100


#Timer spawn of enemy
spawn_enemy = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_enemy, 2000)
enemy_list = []

#Timer spawn of coins
spawn_coin = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_coin, 5000)
coin_list = []


#Font
label = pygame.font.Font("lab_8/lab8_1/Arial.ttf", 60)
lose_label = label.render("You lose", False, (193, 196, 199))
restart_label = label.render("Restart", False, (115, 132, 148))
rect_for_restart = restart_label.get_rect(topleft = (315, 305))

font = pygame.font.SysFont("Arial", 30)

Score = 0

gameplay = True

running = True

while running:
    screen.blit(bg, (0, bg_y + 0))
    screen.blit(bg, (0, bg_y - 650))
    
    if gameplay:
        bg_y += 10
        if bg_y >= 650:
            bg_y = 0
        
        player_rect = Player.get_rect(topleft = (x, y))
        
        
        if enemy_list:
            for (i, el) in enumerate(enemy_list):
                screen.blit(Enemy, el)
                el.y += 12
                
                if el.y > 650:
                    enemy_list.pop(i)
                
                if player_rect.colliderect(el):
                    gameplay = False
        
        if coin_list:
            for (i, el) in enumerate(coin_list):
                screen.blit(Coin, el)
                if player_rect.colliderect(el):
                    Score += 1
                    coin_list.pop(i)
        
        #Random spawn enemy
        Enemy_x = random.randrange(140, 650)
        #Random spawn of coin
        coin_spawn_x = random.randrange(140, 610)
        coin_spawn_y = random.randrange(325, 605)
        #Coins
        coin_rect = Coin.get_rect(topleft = (coin_spawn_x, coin_spawn_y))
        
        #Show player
        screen.blit(Player, (x, y))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            x += 7
            if x > 650:
                x = 650
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            x -= 7
            if x < 140:
                x = 140
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            y += 7
            if y > 630:
                y = 630
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            y -= 3
            if y < 0:
                y = 0
        if pressed[pygame.K_SPACE]:
            y -= 7
            if y < 0:
                y = 0
    
    
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (300, 205))
        screen.blit(restart_label, rect_for_restart)
        
        mouse = pygame.mouse.get_pos()
        if rect_for_restart.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            x = 420
            y = 550
            enemy_list.clear()
            coin_list.clear()
            Score = 0
    
    
    score_text = font.render(f"Score: {Score}", False, "Black")
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 60))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_enemy: #Append enemy_list
            enemy_list.append(Enemy.get_rect(topleft = (Enemy_x, Enemy_y)))
        if event.type == spawn_coin: #Append coin_list
            coin_list.append(Coin.get_rect(topleft = (coin_spawn_x, coin_spawn_y)))
    
    
    pygame.time.Clock().tick(60)
    pygame.display.flip()