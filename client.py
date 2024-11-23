
import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"\n{message}")  # Ensure messages appear on a new line
        except:
            print("\nConnection closed by the server.")
            break

def client():
    client_socket = None
    print("Welcome to the chat client!")
    print("Available commands:")
    print("  CONNECT - Connect to a server")
    print("  SEND <message> - Send a message")
    print("  QUIT - Disconnect from the server and exit")

    while True:
        if not client_socket:
            command = input("Enter command: ").strip()
        else:
            command = input("> ").strip() 

        command_parts = command.split(" ", 1)

        if command_parts[0].upper() == "CONNECT":
            if client_socket:
                print("Already connected to a server.")
                continue

            server_host = input("Enter server IP (e.g., 127.0.0.1): ")
            server_port = int(input("Enter server port (e.g., 12345): "))
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_host, server_port))
                print(f"Connected to server at {server_host}:{server_port}")
                threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
            except Exception as e:
                print(f"Failed to connect: {e}")
                client_socket = None

        elif command_parts[0].upper() == "SEND":
            if not client_socket:
                print("Not connected to any server. Use CONNECT first.")
                continue
            if len(command_parts) < 2:
                print("Please provide a message to send.")
                continue
            message = command_parts[1]
            try:
                client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")
                client_socket = None

        elif command_parts[0].upper() == "QUIT":
            if client_socket:
                try:
                    client_socket.send("Client has left the chat.".encode('utf-8'))
                    client_socket.close()
                except:
                    pass
                print("Disconnected from server.")
                client_socket = None
            print("Exiting chat client.")
            break

        else:
            print("Invalid command. Use CONNECT, SEND <message>, or QUIT.")

if __name__ == "__main__":
    client()
