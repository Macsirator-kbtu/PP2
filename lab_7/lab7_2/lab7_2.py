import pygame
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont('Arial', 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Music files
music_files = [
    r"C:\Users\ivano\PyGames\lab_7\lab7_2\epicsaxguy.mp3",
    r"C:\Users\ivano\PyGames\lab_7\lab7_2\Андрей Губин - Ночь.mp3"
]
current_track = 0

# Key controls
CONTROLS = {
    pygame.K_SPACE: "play/pause",
    pygame.K_s: "stop",
    pygame.K_RIGHT: "next",
    pygame.K_LEFT: "previous"
}

# Load first song
pygame.mixer.music.load(music_files[current_track])

def play_music():
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def next_track():
    global current_track
    current_track = (current_track + 1) % len(music_files)
    pygame.mixer.music.load(music_files[current_track])
    play_music()

def previous_track():
    global current_track
    current_track = (current_track - 1) % len(music_files)
    pygame.mixer.music.load(music_files[current_track])
    play_music()

def draw_interface():
    screen.fill(WHITE)
    
    # Display current track
    track_text = font.render(f"Now Playing: {music_files[current_track]}", True, BLACK)
    screen.blit(track_text, (20, 50))
    
    # Display controls
    controls_text = font.render("Controls: SPACE=Play/Pause, S=Stop, ←=Prev, →=Next", True, BLACK)
    screen.blit(controls_text, (20, 100))
    
    pygame.display.flip()

# Main game loop
running = True
draw_interface()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key in CONTROLS:
                action = CONTROLS[event.key]
                
                if action == "play/pause":
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                        if pygame.mixer.music.get_pos() == -1:  # If not playing
                            play_music()
                
                elif action == "stop":
                    stop_music()
                
                elif action == "next":
                    next_track()
                
                elif action == "previous":
                    previous_track()
                
                draw_interface()

pygame.quit()