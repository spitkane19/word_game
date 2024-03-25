import pygame
import sys
from GameLogic import Game
import time
import yaml
from pygame_widgets.textbox import TextBox
import pygame_widgets
import socket
import json


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
DARKGRAY = (128, 128, 128)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class Button:
    def __init__(self, text, y_position, width = BUTTON_WIDTH, height = BUTTON_HEIGHT):
        self.rect = pygame.Rect((SCREEN_WIDTH - width) // 2, y_position, width, height)
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
                            
                            return single()
                            
                        
                        elif button.text == "Multiplayer":
                            return ConnectionScreen()

        screen.fill(WHITE)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

def draw_word2(guessed_words, square_size, space_between, screen, row,game=None, multi=False, cr_pos = [], cr_let = [], paint=False):
    # Calculate the starting y-coordinate to ensure alignment in the middle
    
    start_y = 10
    if multi:
        word = guessed_words[row]
        # Calculate the total width of the current word
        word_width = len(word) * (square_size + space_between)
        # Calculate the starting x-coordinate to ensure alignment in the middle
        start_x = (SCREEN_WIDTH - word_width) // 2
        result = "".join(word)
        if len(result.replace(" ", "")) != 5:
            correct_positions, correct_letters = [], []
        else:
            correct_positions, correct_letters = cr_pos, cr_let

        for j, letter in enumerate(word):
            rect = pygame.Rect(start_x + j * (square_size + space_between), start_y + row * (square_size + space_between), square_size, square_size)

            # Determine the color based on correct positions and letters
            if paint:
                if j in correct_positions:
                    pygame.draw.rect(screen, GREEN, rect, border_radius=5)

                elif letter in correct_letters:
                    pygame.draw.rect(screen, YELLOW, rect, border_radius=5)
                    
                    
                
                else:
                    pygame.draw.rect(screen, DARKGRAY, rect, border_radius=5)
                    
            else:
                pygame.draw.rect(screen, GRAY, rect, border_radius=5)
                
            font = pygame.font.Font(None, 36)
            text = font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    else:
        for i, word in enumerate(guessed_words):
            # Calculate the total width of the current word
            word_width = len(word) * (square_size + space_between)
            # Calculate the starting x-coordinate to ensure alignment in the middle
            start_x = (SCREEN_WIDTH - word_width) // 2
            result = "".join(word)
            if len(result.replace(" ", "")) != 5:
                correct_positions, correct_letters = [], []
            else:
                correct_positions, correct_letters = game.check_letter(result)

            for j, letter in enumerate(word):
                rect = pygame.Rect(start_x + j * (square_size + space_between), start_y + i * (square_size + space_between), square_size, square_size)

                # Determine the color based on correct positions and letters
                if i != row:
                    if j in correct_positions:
                        pygame.draw.rect(screen, GREEN, rect, border_radius=5)

                    elif letter in correct_letters:
                        pygame.draw.rect(screen, YELLOW, rect, border_radius=5)
                        
                        
                    
                    else:
                        pygame.draw.rect(screen, DARKGRAY, rect, border_radius=5)
                        
                else:
                    pygame.draw.rect(screen, GRAY, rect, border_radius=5)
                    
                font = pygame.font.Font(None, 36)
                text = font.render(letter, True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

keyboard_layout = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']  # Adjusted for double-width buttons
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


def single():
    game = Game()
    word = game.correct_word
    current_row = 0
    # Screen setups
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Singleplayer Wordle")

    clock = pygame.time.Clock()
    running = True

    # Initialize variables for keyboard and guessed words
    start_x = 100
    start_y = 400
    waiting_for_enter = False  # Flag to control when to allow writing to the next row
    guessed_words = []
    if guessed_words == None:
        guessed_words = []
    while len(guessed_words) < 5:
        guessed_words.append('     ')
    word = ""
    draw_word2(guessed_words, 60, 10, screen, game, current_row)
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
                    
                    for i in range(current_row, len(guessed_words)):
                        if " " in guessed_words[i]:
                            word = list(guessed_words[i])
                            for s in range(len(word)):
                                if word[s] == " ":
                                    word[s] = char
                                    result = "".join(word)
                                    guessed_words[i] = result
                                    draw_word2(guessed_words, 60, 10, screen, game, current_row)
                                    pygame.display.flip()
                                    if s == 4:
                                        waiting_for_enter = True

                                    break
                            break
            
            elif event.type == pygame.KEYDOWN:
                
                word = list(guessed_words[current_row])
                result = "".join(word)
                result = result.replace(" ", "")
                s = len(result)
                
                if event.key == pygame.K_RETURN and waiting_for_enter:
                    if s == 5:
                        current_row += 1
                        waiting_for_enter = False
                        draw_word2(guessed_words, 60, 10, screen, game, current_row)
                            
                        pygame.display.flip()
                        if game.did_you_win(result) == 1:
                            time.sleep(2)
                            you_won(game.correct_word)
                        elif current_row == 5:
                            time.sleep(2)
                            you_lost(game.correct_word)
                        
                elif event.key == pygame.K_BACKSPACE:
                    waiting_for_enter = False
                    if len(word) > 0:
                        word[s - 1] = " "
                        s -= 1
                        guessed_words[current_row] = word
                        result = "".join(word)
                        draw_word2(guessed_words, 60, 10, screen, game, current_row)
                        pygame.display.flip()

                elif event.unicode.isalpha() and not waiting_for_enter:
                    char = event.unicode.upper()  # Convert to uppercase
                    for i in range(current_row, len(guessed_words)):
                        if " " in guessed_words[i]:
                            word = list(guessed_words[i])
                            for s in range(len(word)):
                                if word[s] == " ":
                                    word[s] = char
                                    result = "".join(word)
                                    guessed_words[i] = result
                                    draw_word2(guessed_words, 60, 10, screen, game, current_row)
                                    pygame.display.flip()
                                    if s == 4:
                                        waiting_for_enter = True
                                    break
                            break
                break
        #screen.fill(WHITE)
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

def multiplayer(client):
    current_row = 0
    # Screen setups
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Multiplayer Wordle")

    clock = pygame.time.Clock()
    running = True

    # Initialize variables for keyboard and guessed words
    start_x = 100
    start_y = 400
    waiting_for_enter = False  # Flag to control when to allow writing to the next row
    guessed_words = []
    if guessed_words == None:
        guessed_words = []
    while len(guessed_words) < 5:
        guessed_words.append('     ')
    word = ""
    draw_word2(guessed_words, 60, 10, screen, current_row)
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
                    
                    for i in range(current_row, len(guessed_words)):
                        if " " in guessed_words[i]:
                            word = list(guessed_words[i])
                            for s in range(len(word)):
                                if word[s] == " ":
                                    word[s] = char
                                    result = "".join(word)
                                    guessed_words[i] = result
                                    draw_word2(guessed_words, 60, 10, screen, current_row, multi=True)
                                    pygame.display.flip()
                                    if s == 4:
                                        waiting_for_enter = True

                                    break
                            break
            
            elif event.type == pygame.KEYDOWN:
                
                word = list(guessed_words[current_row])
                result = "".join(word)
                result = result.replace(" ", "")
                s = len(result)
                
                if event.key == pygame.K_RETURN and waiting_for_enter:
                    if s == 5:
                        waiting_for_enter = False
                        client.sendall(result.encode('utf-8'))
                        data = client.recv(1024).decode('utf-8')
                        response = json.loads(data)
                        draw_word2(guessed_words, 60, 10, screen, current_row, multi=True, cr_pos = response["correct_positions"], cr_let=response["correct_letters"], paint=True)
                        current_row += 1
                            
                        pygame.display.flip()
                        if response["playing"] == 0:
                            time.sleep(1)
                            waiting(client, game=True)
                
                        
                elif event.key == pygame.K_BACKSPACE:
                    waiting_for_enter = False
                    if len(word) > 0:
                        word[s - 1] = " "
                        s -= 1
                        guessed_words[current_row] = word
                        result = "".join(word)
                        draw_word2(guessed_words, 60, 10, screen, current_row, multi=True)
                        pygame.display.flip()

                elif event.unicode.isalpha() and not waiting_for_enter:

                    char = event.unicode.upper()  # Convert to uppercase
                    for i in range(current_row, len(guessed_words)):
                        if " " in guessed_words[i]:
                            word = list(guessed_words[i])
                            for s in range(len(word)):
                                if word[s] == " ":
                                    word[s] = char
                                    result = "".join(word)
                                    guessed_words[i] = result
                                    draw_word2(guessed_words, 60, 10, screen, current_row, multi=True)
                                    pygame.display.flip()
                                    if s == 4:
                                        waiting_for_enter = True
                                    break
                            break
                break
        #screen.fill(WHITE)
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()


def waiting(client, game=False):
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Waiting for another player")
    screen.fill(WHITE)

    font = pygame.font.Font(None, 36)

    text = font.render("Waiting for other player...", True, BLACK)

    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    # Blit the text onto the screen
    screen.blit(text, text_rect)
    word = ""

    # Update the display
    pygame.display.flip()
    if game:
        while True:
            data = client.recv(1024).decode('utf-8')
            response = json.loads(data)
            message = response["results"]
            word = response["goal"]

            if message == "win":
                return you_won(word, state="WON")
            elif message == "tie":
                return you_won(word, state="TIED")
            else:
                return you_won(word, state="LOSE")
    else:
        while True:
            message = client.recv(1024).decode('utf-8')
            if message == "Start":
                return multiplayer(client)

def ConnectionScreen():
    # Screen setups
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Connect to a Server")

    # Text inputs
    ip_text = "192.168.1.101"
    port_text = "9999"
    name_text = "Username"


    # Text boxes
    name_box = TextBox(screen, 250, 75, 200, 50, fontSize=30, placeholderText=name_text, textColour = BLACK)
    ip_box = TextBox(screen, 250, 175, 200, 50, fontSize=30, placeholderText=ip_text, textColour = BLACK)
    port_box = TextBox(screen, 250, 275, 200, 50, fontSize=30, placeholderText=port_text, textColour = BLACK)

    # Buttons
    back_button = Button("Back", 350, height=80, width=200)
    connect_button = Button("Connect", 450, height=80, width=200)

    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if back button is clicked
                if back_button.rect.collidepoint(mouse_pos):
                    return start()
                # Check if connect button is clicked
                elif connect_button.rect.collidepoint(mouse_pos):
                    if ip_text == "":
                        ip_text = "192.168.1.101"
                    if port_text == "":
                        port_text = "9999"
                    if name_text == "":
                        name_text = "Username"
                    
                    return start_client(ip_text, int(port_text), name_text)
        

        pygame_widgets.update(events)
        # Update text in text boxes
        ip_text = ip_box.getText()
        port_text = port_box.getText()
        name_text = name_box.getText()
        # Draw everything on the screen
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Connect to a Server", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 25))
        ip_label = font.render("IP:", True, BLACK)
        name_lable = font.render("Username: ", True, BLACK)
        screen.blit(ip_label, (130, 175 + ip_box._height // 2 - ip_label.get_height() // 2))
        port_label = font.render("Port:", True, BLACK)
        screen.blit(port_label, (125, 275 + port_box._height // 2 - port_label.get_height() // 2))
        screen.blit(name_lable, (130, 75 + name_box._height // 2 - name_lable.get_height() // 2))

        screen.blit(text, text_rect)
        back_button.draw(screen)
        connect_button.draw(screen)
    
        ip_box.draw()
        port_box.draw()
        name_box.draw()
        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

def you_won(word, state):
    # Screen setup
    print(word)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("You Won!")
    screen.fill(WHITE)  
    font = pygame.font.Font(None, 36)
    text = font.render(f"YOU {state}, THE CORRECT ANSWER WAS {word}", True, (0, 0, 0))
    text_rect = text.get_rect(center=(400, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    
    time.sleep(5)
    
    
    start()

def start_client(host, port, name):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))
    except ConnectionRefusedError or ConnectionError or ConnectionResetError:
        start()

    response = client.recv(1024).decode('utf-8')
    print(response)
    client.sendall(name.encode('utf-8'))
    waiting(client)
    
    
   


if __name__ == "__main__":
    start()