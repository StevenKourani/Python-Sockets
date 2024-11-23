import socket
import threading

clients = []
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            decoded_message = message.decode('utf-8')
            print(f"{client_address} : {decoded_message}")
            broadcast(f"{client_address} : {decoded_message}".encode('utf-8'), client_socket)
        except:
            break

    print(f"Client {client_address} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
