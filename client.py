import socket
import MainMenu
from GameLogic import SinglePlayer
import time
def start_client(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((host, port))

    response = client.recv(1024).decode('utf-8')
    print(response)

    message = str(MainMenu.start())
    
    # Send the message to the server
    client.send(message.encode('utf-8'))
    data = 'correct_letters: []\ncorrect_positions: []\ngame_status: ongoing\nguessed_correctly: false\nguessed_words:\n \nremaining_attempts: 4\n'
    if message == "1": # if singleplayer
        message = (MainMenu.single(data))
        while True:
                # Send the message to the server
                client.send(message.lower().encode('utf-8'))
                # Receive response from the server
                response = client.recv(1024).decode('utf-8')
                print("Server response:", response)
                # Get next word
                message = MainMenu.single(response)

if __name__ == "__main__":
    SERVER_HOST = "127.0.0.1"  # Server IP address
    SERVER_PORT = 9999          # Server port
    start_client(SERVER_HOST, SERVER_PORT)
