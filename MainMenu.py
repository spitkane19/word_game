import pygame
import sys
from GameLogic import SinglePlayer, listofwords
import time
import yaml
from client import current_row

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

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=10)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

def draw_word(word, start_y,screen):
    for i, letter in enumerate(word):
        rect = pygame.Rect(i * BUTTON_WIDTH, start_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, GRAY, rect, border_radius=10)
        font = pygame.font.Font(None, 36)
        text = font.render(letter, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def start():
    # Screen setups
    current_row = 0
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
                        # Singleplayer makes a new game
                        elif button.text == "Singleplayer":
                            return 1
                        
                        elif button.text == "Multiplayer":
                            return 2
                            
                            """ # Create an instance of Singleplayer
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
                                                draw_word(singleplayer.correct_word, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2, screen)
                                                
                                                # Drawing logic for the guessed word
                                                draw_word(singleplayer.guess_word, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT, screen)

                                                # Drawing logic for correct positions and letters
                                                for i, pos in enumerate(correct_positions):
                                                    rect = pygame.Rect(pos * BUTTON_WIDTH, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
                                                    pygame.draw.rect(screen, YELLOW, rect, border_radius=10)

                                                for i, letter in enumerate(correct_letters):
                                                    rect = pygame.Rect(i * BUTTON_WIDTH, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
                                                    pygame.draw.rect(screen, GREEN, rect, border_radius=10)

                                # Your drawing code here (replace with your Pygame drawing logic) """

        screen.fill(WHITE)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

def draw_word2(guessed_words, square_size, space_between, screen, correct_letters, correct_positions):
    # Calculate the starting y-coordinate to ensure alignment in the middle
    start_y = 10

    for i, word in enumerate(guessed_words):
        # Calculate the total width of the current word
        word_width = len(word) * (square_size + space_between)

        # Calculate the starting x-coordinate to ensure alignment in the middle
        start_x = (SCREEN_WIDTH - word_width) // 2

        for j, letter in enumerate(word):
            rect = pygame.Rect(start_x + j * (square_size + space_between), start_y + i * (square_size + space_between), square_size, square_size)

            # Determine the color based on correct positions and letters
            if letter in correct_letters:
                pygame.draw.rect(screen, YELLOW, rect, border_radius=5)
            elif letter in correct_positions:
                pygame.draw.rect(screen, GREEN, rect, border_radius=5)
            else:
                pygame.draw.rect(screen, GRAY, rect, border_radius=5)

            font = pygame.font.Font(None, 36)
            text = font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)




keyboard_layout = [
['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I','J'],
    ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T'],
    ['U', 'V', 'W', 'X', 'Y', 'Z']  # Adjusted for double-width buttons
]

# Define the size and spacing of each key
key_width = 50
key_height = 50
key_spacing = 10

def draw_keyboard(screen, start_x):
    # Calculate the total width of the keyboard
    keyboard_width = len(keyboard_layout[0]) * (key_width + key_spacing)

    # Calculate the starting x-coordinate to ensure alignment in the middle
    start_x = (SCREEN_WIDTH - keyboard_width) // 2

    key_y = 400  # Starting y-coordinate of the keyboard

    for row in keyboard_layout:
        key_x = start_x  # Set the starting x-coordinate for each row
        for char in row:
            # Draw the key
            pygame.draw.rect(screen, (169, 169, 169), (key_x, key_y, key_width, key_height))
            font = pygame.font.Font(None, 36)
            text = font.render(char, True, (0, 0, 0))
            text_rect = text.get_rect(center=(key_x + key_width // 2, key_y + key_height // 2))
            screen.blit(text, text_rect)

            # Move to the next key
            key_x += key_width + key_spacing
        key_y += key_height + key_spacing
        
def get_clicked_key(mouse_pos, start_x, start_y, key_width, key_height, key_spacing):
    char = None
    
    # Iterate over the keyboard layout to check if the mouse click corresponds to a key
    for i, row in enumerate(keyboard_layout):
        key_y = start_y + i * (key_height + key_spacing)  # Calculate key_y based on row index
        for j, key in enumerate(row):
            # Calculate the coordinates of the key's bounding box
            key_x = start_x + j * (key_width + key_spacing)
            key_rect = pygame.Rect(key_x, key_y, key_width, key_height)
            
            # Check if the mouse click is within the bounding box of the key
            if key_rect.collidepoint(mouse_pos):
                row_idx = i
                col_idx = j
                char = key
                return char
    
    return char

def single(data):
    global current_row
    data = yaml.safe_load(data)
    # Parse the YAML response
    correct_letters = data["correct_letters"]
    correct_positions = data["correct_positions"]
    print(correct_positions)
    print("Correct: " + str(correct_positions))
    game_status = data["game_status"]
    guessed_correctly = data["guessed_correctly"]
    if guessed_correctly:
        return "done"
    guessed_words = data["guessed_words"]
    remaining_attempts = data["remaining_attempts"]

    # Screen setups
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Singleplayer Wordle")

    clock = pygame.time.Clock()
    running = True

    # Initialize variables for keyboard and guessed words
    start_x = 100
    start_y = 400
    waiting_for_enter = False  # Flag to control when to allow writing to the next row

    if guessed_words == None:
        guessed_words = []
    while len(guessed_words) < 5:
        guessed_words.append('     ')
    draw_word2(guessed_words, 60, 10, screen, correct_letters, correct_positions)
    draw_keyboard(screen, start_x)
    pygame.display.flip()

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not waiting_for_enter:
                mouse_pos = pygame.mouse.get_pos()
                char = get_clicked_key(mouse_pos, start_x, start_y, key_width, key_height, key_spacing)
                if char:
                    print(f"Pressed letter: {char}")
                    for i in range(current_row, len(guessed_words)):
                        if " " in guessed_words[i]:
                            word = list(guessed_words[i])
                            for s in range(len(word)):
                                if word[s] == " ":
                                    word[s] = char
                                    print(word)
                                    result = "".join(word)
                                    guessed_words[i] = result
                                    draw_word2(guessed_words, 60, 10, screen, correct_letters, correct_positions)
                                    pygame.display.flip()
                                    if s == 4:
                                        waiting_for_enter = True

                                    break
                            break
            elif event.type == pygame.KEYDOWN and waiting_for_enter:
                for i in range(current_row, len(guessed_words)):
                    word = list(guessed_words[i])
                    s = len(word)
                    result = "".join(word)
                    print(word)
                    if event.key == pygame.K_RETURN:
                        print("here")
                        if s == 5:
                            current_row += 1
                            print(current_row)
                            waiting_for_enter = False
                            return result  # Reset the flag to wait for Enter again
                    elif event.key == pygame.K_BACKSPACE:
                        waiting_for_enter = False
                        if len(word) > 0:
                            word[s - 1] = " "
                            s -= 1
                    break
        #screen.fill(WHITE)
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

def waiting():
    pygame.display.set_caption("Waiting for another player")
    pygame.display.flip()

def multi(data):
    global current_row
    waiting_for_enter = False
    data = yaml.safe_load(data)
    # Parse the YAML response
    correct_letters = data["correct_letters"]
    correct_positions = data["correct_positions"]
    print("Correct: " + str(correct_positions))
    game_status = data["game_status"]
    guessed_correctly = data["guessed_correctly"]
    if guessed_correctly:
        start()
        return "done"
    guessed_words = data["guessed_words"]
    remaining_attempts = data["remaining_attempts"]

    # Screen setups
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Multiplayer Wordle")

    clock = pygame.time.Clock()
    running = True

    # Initialize variables for keyboard and guessed words
    start_x = 100
    start_y = 400
    if guessed_words == None:
        guessed_words = []
    while len(guessed_words) < 5:
        guessed_words.append('     ')
    draw_word2(guessed_words, 60, 10, screen,correct_letters,correct_positions)
    draw_keyboard(screen, start_x)
    pygame.display.flip()
    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not waiting_for_enter:
                # Handle mouse write clicks
                mouse_pos = pygame.mouse.get_pos()
                event.type == pygame.KEYDOWN
                char = get_clicked_key(mouse_pos, start_x, start_y, key_width, key_height, key_spacing)
                if char:
                    print(f"Pressed letter: {char}")
                    for i in range(len(guessed_words)):
                        if " " in guessed_words[i]:
                            word = list(guessed_words[i])
                            for s in range(len(word)):
                                if word[s] == " ":
                                    word[s] = char
                                    result = "".join(word)
                                    guessed_words[i]=result
                                    draw_word2(guessed_words, 60, 10, screen,correct_letters,correct_positions)
                                    pygame.display.flip()
                                    if s == 4:
                                        waiting_for_enter = True
                                    
                                    break
                            break
            elif event.type == pygame.KEYDOWN and waiting_for_enter:
                for i in range(current_row, len(guessed_words)):
                    word = list(guessed_words[i])
                    s = len(word)
                    result = "".join(word)
                    print(word)
                    if event.key == pygame.K_RETURN:
                        print("here")
                        if s == 5:
                            current_row += 1
                            print(current_row)
                            waiting_for_enter = False
                            return result  # Reset the flag to wait for Enter again
                            print(result)
                    elif event.key == pygame.K_BACKSPACE:
                        waiting_for_enter = False
                        if len(word) > 0:
                            word[s - 1] = " "
                            s -= 1
                    break


        #screen.fill(WHITE)
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

