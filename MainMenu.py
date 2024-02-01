import pygame
import sys
from GameLogic import Singleplayer, listofwords

pygame.init()
pygame.font.init()

# All the basic constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 100
BUTTON_MARGIN = 60
FPS = 60

WHITE = (251, 252, 248)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class Button:
    def __init__(self, text, y_position):
        self.rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, y_position, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=10)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

def draw_word(word, start_y):
    for i, letter in enumerate(word):
        rect = pygame.Rect(i * BUTTON_WIDTH, start_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, GRAY, rect, border_radius=10)
        font = pygame.font.Font(None, 36)
        text = font.render(letter, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

# Screen setups
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Jenson Buttons
multiplayer_button = Button("Multiplayer", BUTTON_MARGIN)
singleplayer_button = Button("Singleplayer", BUTTON_MARGIN + BUTTON_HEIGHT + BUTTON_MARGIN)
exit_button = Button("Exit", BUTTON_MARGIN + (BUTTON_HEIGHT + BUTTON_MARGIN) * 2)

buttons = [multiplayer_button, singleplayer_button, exit_button]

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    # This is what happens if Exit button is pressed
                    if button.text == "Exit":
                        running = False
                    # Singleplayer makes a new game and makes a new "olio" of Singleplayer
                    elif button.text == "Singleplayer":
                        singleplayer = Singleplayer()  # Create an instance of Singleplayer
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        if singleplayer.check_guess():
                                            print("You are correct!")
                                            # Handle game over logic, e.g., return to the main menu
                                            break
                                        else:
                                            letter = singleplayer.guess_word[0]
                                            correct_positions, correct_letters = singleplayer.check_letter(letter)

                                            # Drawing logic for the word
                                            draw_word(singleplayer.correct_word, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2)
                                            
                                            # Drawing logic for the guessed word
                                            draw_word(singleplayer.guess_word, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT)

                                            # Drawing logic for correct positions and letters
                                            for i, pos in enumerate(correct_positions):
                                                rect = pygame.Rect(pos * BUTTON_WIDTH, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
                                                pygame.draw.rect(screen, YELLOW, rect, border_radius=10)

                                            for i, letter in enumerate(correct_letters):
                                                rect = pygame.Rect(i * BUTTON_WIDTH, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
                                                pygame.draw.rect(screen, GREEN, rect, border_radius=10)

                            # Your drawing code here (replace with your Pygame drawing logic)

    screen.fill(WHITE)

    for button in buttons:
        button.draw()

    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
