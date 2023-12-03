import pygame
import numpy as np
from pydub import AudioSegment

# Function to draw the waveform on the screen
def draw_waveform(surface, data):
    width, height = surface.get_size()
    surface.fill((0, 0, 0))  # Fill the screen with black

    # Scale the data to fit the screen
    data = np.int16(data * height / 2) + height / 2
    data = data[:width]

    # Draw the waveform
    for x in range(1, width):
        pygame.draw.line(surface, (255, 255, 255), (x - 1, data[x - 1]), (x, data[x]), 2)

# Function to draw buttons on the screen
def draw_buttons(screen, play_button, stop_button):
    pygame.draw.rect(screen, (0, 255, 0), play_button)
    pygame.draw.rect(screen, (255, 0, 0), stop_button)

# Function to play the audio file and update the waveform
def play_audio(file_path, screen):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    clock = pygame.time.Clock()

    while pygame.mixer.music.get_busy():
        clock.tick(30)

        # Get the current position in the audio
        pos = pygame.mixer.music.get_pos() / 1000.0

        # Extract the audio data for the next second
        audio_data = np.array(audio[pos * 1000: (pos + 1) * 1000].get_array_of_samples())

        # Normalize the audio data to the range [-1, 1]
        audio_data = audio_data / 32768.0

        # Draw the waveform on the screen
        draw_waveform(screen, audio_data)
        draw_buttons(screen, play_button, stop_button)  # Redraw buttons

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop the audio if the window is closed
                return

    pygame.mixer.music.stop()  # Stop the audio when it finishes

# Load the audio file
file_path = "VundabarAlienBlues.mp3"  # Change this to your audio file
audio = AudioSegment.from_mp3(file_path)

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Audio Visualizer")

# Create play and stop buttons
play_button = pygame.Rect(50, 350, 50, 30)
stop_button = pygame.Rect(120, 350, 50, 30)

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                play_audio(file_path, screen)
            elif stop_button.collidepoint(event.pos):
                pygame.mixer.music.stop()

    # Draw buttons outside of the event loop
    draw_buttons(screen, play_button, stop_button)

    pygame.display.flip()

# Quit Pygame when the window is closed
pygame.quit()
