import socket
import threading
import yaml
import os
from GameLogic import Game
import time
import random
import json

five_letter_words = [
    "APPLE", "BREAD", "CHAOS", "DOZEN", "EGRET", "FAITH", "GRACE", "HELLO", "IGLOO", "JOKER",
    "KIWI", "LEMON", "MANGO", "NINJA", "OCEAN", "PIZZA", "QUACK", "ROBOT", "SMILE", "TIGER",
    "UMBRA", "VOICE", "WOMAN", "XYLAN", "YACHT", "ZEBRA", "ADOPT", "BENCH", "CRISP", "DREAM",
    "ELBOW", "FLASK", "GRAND", "HUMOR", "IVORY", "JEWEL", "KNOCK", "LIGHT", "MIRTH", "NEVER",
    "OPERA", "PRIZE", "QUEST", "ROCKY", "SHINE", "TWEET", "UNCLE", "VOWEL", "WATER", "XENON",
    "YIELD", "ZESTY", "ALARM", "BLISS", "CRAFT", "DELUX", "ENERG", "FABLE", "GURUS", "HEART",
    "IMAGE", "JUMPS", "KINGS", "LUNAR", "MONEY", "NIGHT", "OLIVE", "PEACH", "QUICK", "RAVEN",
    "SAUCE", "TANGO", "UNZIP", "VIDEO", "WAVES", "XENIA", "YOGIC", "ZINCH", "ABOUT", "BIRTH",
    "CHAIR", "DAISY", "EAGLE", "FRAME", "GLAZE", "HONEY", "INPUT", "JOKES", "KAYAK", "LEMON",
    "MAGIC", "NOBLE", "OUTER", "PEAKS", "QUIRK", "RADIO", "SALAD", "TOAST", "UNITY", "VENOM",
    "WILLY", "XENIA", "YACHT", "ZEBRA", "ALBUM", "BLUSH", "CATCH", "DINGY", "ELITE", "FILMS",
    "GRASP", "HASTE", "IVIES", "JUMPY", "KNIFE", "LUNCH", "MUMMY", "NOISE", "OZONE", "PRISM",
    "QUACK", "RANCH", "SLEEP", "TRUST", "URBAN", "VIXEN", "WASTE", "XENON", "YOUTH", "ZEBRA",
    "ABIDE", "BRAVE", "CLOUD", "DANCE", "EAGER", "FLIRT", "GHOST", "HUMAN", "ICING", "JAZZY",
    "KICKS", "LOVER", "MUSIC", "NIGHT", "ORBIT", "PLUTO", "QUIET", "RAISE", "SHINE", "TIGER",
    "USHER", "VALUE", "WORLD", "XENON", "YACHT", "ZOOMS"
]


gamer_list = []
game_state_file = "GameState.yaml"
game_flags=[0,0]
guesses = [0,0]
lock = threading.Lock()


def create_player_state(address):
    # Path to the GameState.yaml file
    if not os.path.exists(game_state_file):
        # If the file doesn't exist, create it with an empty players dictionary
        with open(game_state_file, 'w') as f:
            yaml.dump({"players": {}}, f)

    # Load the current game state
    with open(game_state_file, 'r') as f:
        game_state = yaml.safe_load(f)

    # Create a new player state
    new_player_state = {
    "opponent": None,  # Add opponent field
    "correct_letters": [],
    "correct_positions": [],
    "game_status": "ongoing",
    "guessed_correctly": False,
    "guessed_words": [],
    "remaining_attempts": 5,
    }
    
    # Add the new player to the game state
    game_state["players"][f"player_{address[1]}"] = new_player_state

    # Write the updated game state back to the file
    with open(game_state_file, 'w') as f:
        yaml.dump(game_state, f)

    return game_state

def handle_client(client_socket, address, game):
    global gamer_list
    word = game.get_correct_word()
    playing = 1
    index = gamer_list.index((client_socket, address))
    game_flags[index] = 0
    guesses[index] = 0
    while True:
        try:
            # Acquire the lock before accessing shared resources
            data = client_socket.recv(1024).decode('utf-8')
            while lock.locked():
                time.sleep(0.1)
            with lock:
                guesses[index] += 1

                # Check game state and update flags
                if game.did_you_win(data) or guesses[index] == 5:
                    game_flags[index] = 1
                    playing = 0
                if guesses[index] == 5:
                    game_flags[index] = -1
                    playing = 0
            
                # Send game state to client
            correct_positions, correct_letters = game.check_letter(data)
            message = {
                "correct_positions": correct_positions,
                "correct_letters": correct_letters,
                "playing": playing
            }
            message_json = json.dumps(message)
            client_socket.sendall(message_json.encode('utf-8'))

                # Process end of game logic
            if playing == 0:
                # Release the lock while waiting for other clients
                time.sleep(1)
                while 0 in game_flags:
                    time.sleep(1)
                while lock.locked():
                    time.sleep(0.1)

                # Acquire the lock again before updating flags and sending messages
                with lock:
                    if game.did_you_win(data):
                        game_flags[index] = 1
                    if guesses[index] == 5:
                        game_flags[index] = -1
                    if guesses[index] == guesses[index - 1]:
                        txt = "tie"
                    elif guesses[index] > guesses[index - 1]:
                        txt = "lose"
                    else:
                        txt = "win"
                    message = {
                        "results": txt,
                        "goal": word
                    }
                    message_json = json.dumps(message)
                    client_socket.sendall(message_json.encode('utf-8'))
                time.sleep(5)
                disconnect(client_socket, address)
                break
                # Release the lock after sending messages
                

            if not data:
                print(f"[*] Connection closed by {address}")
                break
            print(f"[*] Received data from {address}: {data}")

        except ConnectionResetError:
            print(f"[*] Connection reset by {address}")
            break

    client_socket.close()
def disconnect(client, address):
    global gamer_list
    for i, (client_socket, addr) in enumerate(gamer_list):
        if client_socket == client and addr == address:
            # Close the client socket
            client_socket.close()
            # Remove the client from the gamer_list
            del gamer_list[i]
            break

def add_player(client_socket, address):
    global gamer_list
    gamer_list.append((client_socket,address))
    if len(gamer_list) == 1:
        text = "Wait"
        client_socket.sendall(text.encode('utf-8'))
    else:
        start_game()

def start_game():
    word = random.choice(five_letter_words)
    game = Game(word=word)
    for client_socket, address in gamer_list:
        text = "Start"
        client_socket.sendall(text.encode('utf-8'))

    # Start handling client messages concurrently
    for client_socket, address in gamer_list:
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address, game))
        client_handler.start()

                


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    try:
        while True:
            client, address = server.accept()
            print(f"[*] Accepted connection from {address[0]}:{address[1]}")

            # Create player state file
            game_state = create_player_state(address)
            text = "Hello, you have connected to the server!"
            client.sendall(text.encode('utf-8'))
            name = client.recv(1024).decode('utf-8')

            # Handle the client's connection
            client_handler = threading.Thread(target=add_player, args=(client, address))
            client_handler.start()

    except KeyboardInterrupt:
        print("\n[*] Exiting server...")
        server.close()

if __name__ == "__main__":
    HOST = "192.168.1.101"  # Listen on all interfaces
    PORT = 9999       # Choose an appropriate port
    start_server(HOST, PORT)