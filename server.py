import socket
import threading
import yaml
import os
from GameLogic import Game
import time

gamer_list = []
game_state_file = "GameState.yaml"

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
    print(game_state)
    print(address)
    # Add the new player to the game state
    game_state["players"][f"player_{address[1]}"] = new_player_state

    # Write the updated game state back to the file
    with open(game_state_file, 'w') as f:
        yaml.dump(game_state, f)

    return game_state

def handle_client(client_socket, address, game):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if game.did_you_win(data):
                text = "Wait"

            if not data:
                print(f"[*] Connection closed by {address}")
                break
            print(f"[*] Received data from {address}: {data}")
            
            # Process the received data (implement your message handling logic here)
            
        except ConnectionResetError:
            print(f"[*] Connection reset by {address}")
            break
        
    client_socket.close()

def add_player(client_socket, address):
    gamer_list.append((client_socket,address))
    if len(gamer_list) == 1:
        text = "Wait"
        client_socket.sendall(text.encode('utf-8'))
    else:
        start_game()

def start_game():
    game = Game()
    correct_answer = game.get_correct_word()
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
    global server_running
    server_running = 1
    try:
        while server_running:
            client, address = server.accept()
            print(f"[*] Accepted connection from {address[0]}:{address[1]}")

            # Create player state file
            game_state = create_player_state(address)

            # Handle the client's connection
            client_handler = threading.Thread(target=add_player, args=(client, address))
            client_handler.start()

    except KeyboardInterrupt:
        print("\n[*] Exiting server...")
        server_running = 0
        server.close()

if __name__ == "__main__":
    HOST = "192.168.1.101"  # Listen on all interfaces
    PORT = 9999       # Choose an appropriate port
    start_server(HOST, PORT)