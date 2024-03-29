import socket
import MainMenu
from GameLogic import SinglePlayer
import time
global current_row
current_row = 0

def start_client(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((host, port))

    response = client.recv(1024).decode('utf-8')

    message= str(MainMenu.start())
    message_tuple = eval(message)
    print("message= " + str(message_tuple[0]))
    print("name= " + str(message_tuple[1]))
    # Send the message to the server
    client.send(message.encode('utf-8'))
    message = str(message_tuple[0])
    #data = 'correct_letters: []\ncorrect_positions: []\ngame_status: ongoing\nguessed_correctly: false\nguessed_words:\n \nremaining_attempts: 4\n'
    current_row = 0
    if message == "1": # if singleplayer
        response = client.recv(1024).decode('utf-8')
        message = str(MainMenu.single(response))
        while True:
                # Send the message to the server
                print("viesti: " + message)
                client.send(message.lower().encode('utf-8'))
                # Receive response from the server
                response = client.recv(1024).decode('utf-8')
                if response == "done":
                    print("done")
                    break

                print("Server response:", response)
                # Get next word
                message = MainMenu.single(response)
    elif message == "2":
        data = 'correct_letters: []\ncorrect_positions: []\ngame_status: ongoing\nguessed_correctly: false\nguessed_words:\n \nremaining_attempts: 4\n '

        response = client.recv(1024).decode('utf-8')
        print(response)
        if response == "Wait":
            MainMenu.waiting()

        # Keep checking for "Ready" in a loop
            while True:
                response = client.recv(1024).decode('utf-8')
                print(response)

                if response == "Ready":
                    print("Ready received. Exiting loop.")
                    break

                time.sleep(1)
        message = (MainMenu.multi(data))
        while True:           
            print("Loopink")
            client.send(message.lower().encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            if response == "finish":
                response = client.recv(1024).decode('utf-8')
                if response == 1:
                    print("It's a tie")
                else:
                    print("Winner is : " + str(response))
            print("Server response:", response)
            if message == "done":
                print('done')
            message = (MainMenu.multi(data))
    elif message == "4":
        client.send(message.lower().encode('utf-8'))
        print("ass")   
        response = client.recv(1024).decode('utf-8')
        message = str(MainMenu.single(response))
        while True:
            # Send the message to the server
            print("viesti: " + message)
            client.send(message.lower().encode('utf-8'))
            # Receive response from the server
            response = client.recv(1024).decode('utf-8')
            if response == "done":
                print("done")
                break

            print("Server response:", response)
            # Get next word
            message = MainMenu.single(response)

if __name__ == "__main__":
    SERVER_HOST = "192.168.1.102"  # Server IP address
    SERVER_PORT = 9999          # Server port
    start_client(SERVER_HOST, SERVER_PORT)
