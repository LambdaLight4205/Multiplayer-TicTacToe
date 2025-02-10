import socket
import threading
from colorama import Fore, Style, init

init(autoreset=True) # Initialise colorama

# choisit les couleurs
MY_COLOR = Fore.CYAN
OTHER_COLOR = Fore.YELLOW

# fonction pour envoyer des messages au serveur
def send_message(client_socket):
    while True:
        message = input(f"{MY_COLOR}You → {Style.RESET_ALL}")
        client_socket.send(message.encode())

# fonction pour recevoir des messages du serveur
def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"{OTHER_COLOR}Other → {message.decode()}{Style.RESET_ALL}")
                print(f"{MY_COLOR}You → {Style.RESET_ALL}")
        except:
            break

# setup du client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '127.0.0.1'  # IP du serveur
server_port = 12345      # port du serveur

# connexion au serveur
client_socket.connect((server_ip, server_port))

# lance des threads pour envoyer et recevoir des messages
receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
receive_thread.start()

send_thread = threading.Thread(target=send_message, args=(client_socket,))
send_thread.start()
