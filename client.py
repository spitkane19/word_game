import pygame
import sys
import time
import yaml,json
from pygame_widgets.textbox import TextBox
import pygame_widgets
import socket

pygame.init()
pygame.font.init()

# All the basic constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 100
BUTTON_MARGIN = 40
TEXTBOX_WIDTH = 200
TEXTBOX_HEIGHT = 35
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

class TextBox1:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = pygame.font.Font(None, 36)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        color = BLACK if self.active else GRAY
        pygame.draw.rect(screen, color, self.rect, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

def draw_word(word, start_y,screen):
    for i, letter in enumerate(word):
        rect = pygame.Rect(i * BUTTON_WIDTH, start_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, GRAY, rect, border_radius=10)
        font = pygame.font.Font(None, 36)
        text = font.render(letter, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def start(client):
    # Screen setups
    current_row = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    # Jenson Buttons
    text_box = TextBox1((SCREEN_WIDTH - TEXTBOX_WIDTH) // 2, 40, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
    multiplayer_button = Button("Multiplayer", BUTTON_MARGIN + 40)
    singleplayer_button = Button("Singleplayer", BUTTON_MARGIN + BUTTON_HEIGHT + BUTTON_MARGIN+ 40)
    exit_button = Button("Exit", BUTTON_MARGIN + (BUTTON_HEIGHT + BUTTON_MARGIN) * 2+ 40)
    reconnect_button = Button("Reconnect", BUTTON_MARGIN + (BUTTON_HEIGHT + BUTTON_MARGIN) * 3 + 40)

    buttons = [multiplayer_button, singleplayer_button, exit_button, reconnect_button]

    clock = pygame.time.Clock()
    running = True

    while running:
        text_empty = len(text_box.text.strip()) == 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not text_empty:
                    for button in buttons:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            name = text_box.text.strip()
                            # This is what happens if Exit button is pressed
                            if button.text == "Exit":
                                running = False
                            # Singleplayer makes a new game
                            elif button.text == "Singleplayer":
                                return single(client,name)
                            elif button.text == "Multiplayer":
                                return ConnectionScreen()
                            elif button.text == "Reconnect":
                                gamestate = Reconnect(client,name) # TODO täällä gamestatessa on nyt vanhan pelin tiedot
                                print(gamestate)
                                return ConnectionScreen()
            text_box.handle_event(event)
                            
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text_surface = font.render("First write your name", True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(text_surface, text_rect)
        for button in buttons:
            button.draw(screen)
        text_box.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

def Reconnect(client,name):
    print("getting game info from server")
    message = "Reconnect" + " " + name
    client.send(message.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    return response

def draw_word2(client,guessed_words, square_size, space_between, screen, row, multi=False, cr_pos = [], cr_let = []):
    # Calculate the starting y-coordinate to ensure alignment in the middle
    
    start_y = 10
    if multi:
        for i, word in enumerate(guessed_words):
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
                message = "check_letter" + " " + str(result)
                client.send(message.encode('utf-8'))
                correct_positions = client.recv(1024).decode('utf-8')
                correct_letters = client.recv(1024).decode('utf-8')

            for j, letter in enumerate(word):
                rect = pygame.Rect(start_x + j * (square_size + space_between), start_y + i * (square_size + space_between), square_size, square_size)

                # Determine the color based on correct positions and letters
                if i != row:
                    if str(j) in correct_positions:
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

def single(client, name):
    message = "correct_word"
    client.send(message.encode('utf-8'))
    salasana = client.recv(1024).decode('utf-8')
    current_row = 0
    # Screen setups
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Singleplayer Wordle")

    clock = pygame.time.Clock()
    running = True
    message = "new_player" + " " + name
    client.send(message.encode('utf-8'))

    # Receive player state from the server
    response = client.recv(1024).decode('utf-8')
    player_state = yaml.safe_load(response)
    print(player_state)

    # Find the player UUID with the matching nickname
    player_uuid = None
    players = player_state.get("players", {})
    for uuid, data in players.items():
        print(f"UUID: {uuid}, Data: {data}")
        if data and data.get("nickname") == name:
            player_uuid = uuid
            break
    print("Player UUID:", player_uuid)

    print("uuid: " + str(player_uuid))
    message = "update"
    client.sendall(yaml.dump(message).encode('utf-8'))
    print("salasana: " + salasana[0:5])
    message = {"player_uuid": player_uuid, "modifications": {"correct_word": salasana[0:5]}}
    print(message)
    message_str = json.dumps(message)
    message_bytes = message_str.encode('utf-8')
    client.sendall(message_bytes)
    start_x = 100
    start_y = 400
    waiting_for_enter = False  # Flag to control when to allow writing to the next row
    guessed_words = []
    if guessed_words == None:
        guessed_words = []
    while len(guessed_words) < 5:
        guessed_words.append('     ')
    word = ""
    draw_word2(client, guessed_words, 60, 10, screen, current_row)
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
                                    draw_word2(client, guessed_words, 60, 10, screen, current_row)
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
                        draw_word2(client, guessed_words, 60, 10, screen, current_row)
                        pygame.display.flip()
                        message = "did_you_win" + " " + str(result)
                        client.send(message.encode('utf-8'))
                        response = client.recv(1024).decode('utf-8')
                        # Update game state and send to the server
                        client.send(message.encode('utf-8'))
                        response = client.recv(1024).decode('utf-8')
                        word = response  # game.correct_word #TODO
                        message = "update"
                        message = {"player_uuid": player_uuid, "modifications": {"guessed_words": guessed_words}} # TODO tämän lähetys/vastaanotto ei toimi
                        print(message)
                        message_str = json.dumps(message)
                        message_bytes = message_str.encode('utf-8')
                        client.sendall(message_bytes)
                        _ = client.recv(1024).decode('utf-8')
                        _ = yaml.safe_load(_)

                        if response == "1":
                            time.sleep(2)
                            message = "correct_word"
                            client.send(message.encode('utf-8'))
                            response = client.recv(1024).decode('utf-8')
                            you_won(response[0:5], client)
                        elif current_row == 5:
                            time.sleep(2)
                            message = "correct_word"
                            client.send(message.encode('utf-8'))
                            response = client.recv(1024).decode('utf-8')
                            you_lost(response[0:5], client)
                elif event.key == pygame.K_BACKSPACE:
                    waiting_for_enter = False
                    if len(word) > 0:
                        word[s - 1] = " "
                        s -= 1
                        guessed_words[current_row] = word
                        result = "".join(word)
                        draw_word2(client, guessed_words, 60, 10, screen, current_row)
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
                                    draw_word2(client, guessed_words, 60, 10, screen, current_row)
                                    pygame.display.flip()
                                    if s == 4:
                                        waiting_for_enter = True
                                    break
                            break
                break
        # screen.fill(WHITE)
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

def waiting():
    pygame.display.set_caption("Waiting for another player")
    pygame.display.flip()

def ConnectionScreen():
    # Screen setups
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Connect to a Server")

    # Text inputs
    ip_text = "192.168.1.101"
    port_text = "9999"

    # Text boxes
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
                    return start_client(ip_text, int(port_text))
        
        pygame_widgets.update(events)
        # Update text in text boxes
        ip_text = ip_box.getText()
        port_text = port_box.getText()
        # Draw everything on the screen
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Connect to a Server", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        ip_label = font.render("IP:", True, BLACK)
        screen.blit(ip_label, (130, 175 + ip_box._height // 2 - ip_label.get_height() // 2))
        port_label = font.render("Port:", True, BLACK)
        screen.blit(port_label, (125, 275 + port_box._height // 2 - port_label.get_height() // 2))
        screen.blit(text, text_rect)
        back_button.draw(screen)
        connect_button.draw(screen)
        ip_box.draw()
        port_box.draw()
        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

def you_won(word,client):
    # Screen setup
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("You Won!")
    screen.fill(WHITE)  
    font = pygame.font.Font(None, 36)
    text = font.render(f"YOU WON, THE CORRECT ANSWER WAS {word}", True, (0, 0, 0))
    text_rect = text.get_rect(center=(400, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(5)
    start(client)

def you_lost(word,client):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("You Lost!")
    screen.fill(WHITE) 
    font = pygame.font.Font(None, 36)
    text = font.render(f"YOU LOST, THE CORRECT ANSWER WAS {word}", True, (0, 0, 0))
    text_rect = text.get_rect(center=(400, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(5)
    start(client)

def start_client(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((host, port))
    message = "hey"
    client.send(message.encode('utf-8'))
    start(client)
    
if __name__ == "__main__":
    SERVER_HOST = "192.168.1.102"  # Server IP address
    SERVER_PORT = 9999          # Server port
    start_client(SERVER_HOST, SERVER_PORT)
