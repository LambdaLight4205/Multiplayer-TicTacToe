import socket
import threading

# liste des clients connectés
clients = []

# fonction pour gérer la communication entre les clients
def handle_client(client_socket, client_adress):
    # ajoute le client à la liste
    clients.append(client_socket)
    print(f'Client {client_adress} est connecté')

    try:
        while True:
            message = client_socket.recv(1024) # récupère le message envoyé par le client
            if not message: # déconnexion du client
                break

            msg = message.decode()
            print(f'Message reçu de {client_adress} : {msg}')

            # envoie le message à chaque autre client connecté
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(message)
                    except:
                        pass # ignore les erreurs

    except Exception as e:
        print(f'Erreur : {e}')
    
    finally:
        clients.remove(client_socket)
        client_socket.close()
        print(f'Client {client_adress} est déconnecté')

# setup du serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0' # écoute sur toutes les interfaces disponibles
port = 12345

server_socket.bind((host, port))
server_socket.listen(2) # limite l'écoute à deux clients
print(f'Le serveur écoute {host}:{port}...')

# accepte deux clients et crée un thread pour chacun
while len(clients) < 2:
    client_socket, client_adress = server_socket.accept()
    
    # démarre un thread pour gérer le client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_adress))
    client_thread.start()