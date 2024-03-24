import socket
import threading
import yaml
import os,json
from GameLogic import Game
import uuid  # Import the UUID module
import struct

gamer_list = []
game_state_file = "GameState.yaml"

def create_player_state(address, name):
    # Generate a UUID for the player
    player_uuid = str(uuid.uuid4())

    # Load the current game state
    with open(game_state_file, 'r') as f:
        game_state = yaml.safe_load(f)

    # Create a new player state
    new_player_state = {
        "ip_address": address[0],  # Save only the IP address as a string
        "nickname": name,
        "correct_letters": [],
        "correct_positions": [],
        "game_status": "ongoing",
        "guessed_correctly": False,
        "guessed_words": [],
        "remaining_attempts": 5,
        "correct_word": ""  # Initialize correct_word as empty string
    }
    
    # Add the new player to the game state with the generated UUID as the key
    game_state["players"][player_uuid] = new_player_state

    # Write the updated game state back to the file
    with open(game_state_file, 'w') as f:
        yaml.dump(game_state, f)

    return game_state

def modify_player_state(data):
    print("modifying")
    # Load the current game state
    with open(game_state_file, 'r') as f:
        game_state = yaml.safe_load(f)

    # Extract player UUID and modification data from the input
    player_uuid = data.get("player_uuid")
    modifications = data.get("modifications", {})

    # Check if the player UUID and modifications are provided
    if player_uuid is None or not isinstance(modifications, dict):
        return  # Exit if essential data is missing or invalid

    # Check if the player UUID exists in the game state
    if player_uuid not in game_state.get("players", {}):
        return  # Exit if the player UUID is not found

    # Update the player state with the provided modifications
    player_state = game_state["players"][player_uuid]
    player_state.update(modifications)

    # Write the updated game state back to the file
    with open(game_state_file, 'w') as f:
        yaml.dump(game_state, f)
    print("done")
    return game_state

def handle_client(client_socket, address, game):
    game = Game()
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                data = data.split()
                print(data)
                try:
                    if data[0] == "correct_word":
                        message = game.correct_word
                        client_socket.sendall(yaml.dump(message).encode('utf-8'))
                    elif data[0] == "check_letter":
                        correct_positions, correct_letters = game.check_letter(data[1])
                        client_socket.sendall(yaml.dump(correct_positions).encode('utf-8'))
                        client_socket.sendall(yaml.dump(correct_letters).encode('utf-8'))
                    elif data[0] == "did_you_win":
                        message = game.did_you_win(data[1])
                        client_socket.sendall(yaml.dump(message).encode('utf-8'))
                    elif data[0] == "Reconnect":
                        print("Reconnecting")
                        player_data = load_player_data(data[1])
                        if player_data:
                            client_socket.sendall(yaml.dump(player_data).encode('utf-8'))
                        else:
                            print("No data found")
                            client_socket.sendall(b"Player data not found")
                    elif data[0] == "new_player":
                        game_state = create_player_state(address[0],data[1])
                        client_socket.sendall(yaml.dump(game_state).encode('utf-8'))
                    elif data[0] == "update": # TODO Ei toimi json lataus tässä, tämä laittaa arvatun sanan tiedot tietokantaan
                        received_bytes = client_socket.recv(1024)
                        received_str = received_bytes.decode('utf-8')
                        received_message = json.loads(received_str)
                        game_state = modify_player_state(received_message)
                        client_socket.sendall(yaml.dump(game_state).encode('utf-8'))
                except IndexError:
                    continue
        except ConnectionResetError:
            # ConnectionResetError indicates that the client has abruptly closed the connection
            print(f"[*] Connection reset by {address[0]}")
            # Close the client socket and exit the loop
            client_socket.close()
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

def load_player_data(nickname):
    with open(game_state_file, "r") as file:
        data = yaml.safe_load(file)
        # Iterate through each player
        for player_uuid, player_data in data.get("players", {}).items():

            # Check if IP address and nickname match
            if player_data["nickname"] == nickname:
                return player_data
                
    return None  # Return None if player data is not found

def check_name_in_file(nickname):
    with open(game_state_file, "r") as file:
        data = yaml.safe_load(file)
        # Check if the name is present in the file
        for player_uuid, player_data in data.get("players", {}).items():
            if player_data["nickname"] == nickname:
                return True
                
    return False  # Return False if name is not found

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    try:
        while True:
            client, address = server.accept()
            print(f"[*] Accepted connection from {address[0]}")

            # Create player state file

            game_state = create_player_state(address,"None")
                        
            # Handle the client's connection
            client_handler = threading.Thread(target=handle_client, args=(client, address,game_state))
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[*] Exiting server...")
        server.close()

if __name__ == "__main__":
    HOST = "192.168.1.102"  # Listen on all interfaces
    PORT = 9999       # Choose an appropriate port
    start_server(HOST, PORT)