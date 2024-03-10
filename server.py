import socket
import threading
import yaml
import os
from GameLogic import SinglePlayer,Multiplayer
multiplayer_counter = 0
clients = []
def create_player_state(address):
    # Path to the GameState.yaml file
    game_state_file = "GameState.yaml"

    if not os.path.exists(game_state_file):
        # If the file doesn't exist, create it with an empty players dictionary
        with open(game_state_file, 'w') as f:
            yaml.dump({"players": {}}, f)

    # Load the current game state
    with open(game_state_file, 'r') as f:
        game_state = yaml.safe_load(f)

    # Create a new player state
    new_player_state = {
    "correct_letters": [],
    "correct_positions": [],
    "game_status": "ongoing",
    "guessed_correctly": False,
    "guessed_words": [],
    "remaining_attempts": 5,
    "player_number" : ""
    }

    # Add the new player to the game state
    game_state["players"][f"player_{address[1]}"] = new_player_state

    # Write the updated game state back to the file
    with open(game_state_file, 'w') as f:
        yaml.dump(game_state, f)

def handle_client(client_socket, address):
    global multiplayer_counter
    choice_options = "Choose an option:\n1. Singleplayer\n2. Multiplayer\n3. Quit\n"
    client_socket.sendall(choice_options.encode('utf-8'))
    while True:
        # Receive choice from the client
        choice = client_socket.recv(1024).decode('utf-8')

        # Process client choice
        if choice == "1":  # Singleplayer
            singleplayer = SinglePlayer()
            target_word = singleplayer.get_correct_word()
            print(target_word)
            break
        elif choice == "2":  # Multiplayer
            print(multiplayer_counter)
            if multiplayer_counter % 2 == 0:  # Check if even
                multiplayer = Multiplayer()
                # Start a new game
                clients.append(client_socket)

                multiplayer.start_game(False)
                text = "Wait"
                client_socket.sendall(text.encode('utf-8'))
                multiplayer_counter += 1
                return
            else:
                # Add player to existing game
                multiplayer = Multiplayer()
                clients.append(client_socket)
                print("second player here")
                text = "Ready"
                print("Ass")
                for client in clients:
                    client.sendall(text.encode('utf-8'))
                multiplayer.start_game(True)
                print("started game")
                target_word = multiplayer.get_correct_word()
                print(target_word)
            multiplayer_counter += 1  # Increment counter
            break
        elif choice == "3":  # Quit
            client_socket.close()
            return
        else:
            # Invalid choice, send error message to client
            error_message = "Invalid choice. Please choose again."
            client_socket.sendall(error_message.encode('utf-8'))
    
    if choice == "1":
        # Load the game state
        game_state_file = "GameState.yaml"
        if not os.path.exists(game_state_file):
            # If the file doesn't exist, send an empty state to the client
            client_socket.sendall(yaml.dump({"players": {}}).encode('utf-8'))
            return

        with open(game_state_file, 'r') as f:
            game_state = yaml.safe_load(f)

        # Retrieve the player state from the game state
        player_state = game_state["players"].get(f"player_{address[1]}", None)

        if player_state is None:
            # If player state doesn't exist, create a new one
            print("target" + str(target_word))
            create_player_state(address)
            with open(game_state_file, 'r') as f:
                game_state = yaml.safe_load(f)
            player_state = game_state["players"][f"player_{address[1]}"]

        while True:
            # Receive guess from the client
            guess = client_socket.recv(1024).decode('utf-8')
            # Check if the guess is correct
            guessed_correctly = singleplayer.check_guess(guess)

            correct_positions, correct_letters = singleplayer.check_letter(guess)
            # Update guessed words and remaining attempts
            player_state["guessed_words"].append(guess)
            player_state["remaining_attempts"] -= 1

            # Update game status
            player_state["player_number"] = ""
            player_state["guessed_correctly"] = guessed_correctly
            player_state["correct_positions"] = [guess,correct_positions]
            player_state["correct_letters"] = correct_letters
            if player_state["remaining_attempts"] == 0 or player_state["guessed_correctly"]:
                player_state["game_status"] = "ended"

            # Write the updated game state back to the file
            with open(game_state_file, 'w') as f:
                yaml.dump(game_state, f)

            client_socket.sendall(yaml.dump(player_state).encode('utf-8'))

    elif choice == "2":
         # Load the game state
        game_state_file = "GameState.yaml"
        if not os.path.exists(game_state_file):
            # If the file doesn't exist, send an empty state to the client
            client_socket.sendall(yaml.dump({"players": {}}).encode('utf-8'))
            return

        with open(game_state_file, 'r') as f:
            game_state = yaml.safe_load(f)

        # Retrieve the player state from the game state
        player_state = game_state["players"].get(f"player_{address[1]}", None)

        if player_state is None:
            # If player state doesn't exist, create a new one
            print("target" + str(target_word))
            create_player_state(address)
            with open(game_state_file, 'r') as f:
                game_state = yaml.safe_load(f)
            player_state = game_state["players"][f"player_{address[1]}"]

        while True:
            # Receive guess from the client
            guess = client_socket.recv(1024).decode('utf-8')
            # Check if the guess is correct
            guessed_correctly = multiplayer.check_guess(guess)

            correct_positions, correct_letters = multiplayer.check_letter(guess)
            # Update guessed words and remaining attempts
            player_state["guessed_words"].append(guess)
            player_state["remaining_attempts"] -= 1

            # Update game status
            player_state["player_number"] = multiplayer_counter
            player_state["guessed_correctly"] = guessed_correctly
            player_state["correct_positions"] = [guess,correct_positions]
            player_state["correct_letters"] = correct_letters
            if player_state["remaining_attempts"] == 0 or player_state["guessed_correctly"]:
                player_state["game_status"] = "ended"

            # Write the updated game state back to the file
            with open(game_state_file, 'w') as f:
                yaml.dump(game_state, f)
                
            client_socket.sendall(yaml.dump(player_state).encode('utf-8'))

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
            create_player_state(address)

            # Handle the client's connection
            client_handler = threading.Thread(target=handle_client, args=(client, address))
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[*] Exiting server...")
        server.close()

if __name__ == "__main__":
    HOST = "192.168.1.102"  # Listen on all interfaces
    PORT = 9999       # Choose an appropriate port
    start_server(HOST, PORT)
