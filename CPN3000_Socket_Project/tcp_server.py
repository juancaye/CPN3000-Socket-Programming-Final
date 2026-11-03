
import socket
import ssl

# Configure the server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12001
BUFFER_SIZE = 1024

# Create TCP server
def start_server():
    server = None

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket
        server.bind((SERVER_IP, SERVER_PORT))
        server.listen(5)
        server.settimeout(1)

        print("TCP server is running...")

        # Accept incoming connections
        while True:
            try:
                connection, client_address = server.accept()
            except socket.timeout:
                continue

            print(f"Connected to: {client_address}")

            # Handle client communication
            with connection:
                connection.settimeout(5)

                try:
                    data = connection.recv(BUFFER_SIZE)

                    if not data:
                        print("Client disconnected.")
                        continue

                    try:
                        message = data.decode("utf-8")
                    except UnicodeDecodeError:
                        print("Error: Invalid message encoding.")
                        continue

                    if not message.strip():
                        print("Error: Empty message received.")
                        continue

                    print(f"Received: {message}")

                    # Echo the message
                    connection.sendall(data)
                    print("Message echoed successfully.")

                except socket.timeout:
                    print("Error: Client communication timed out.")

                except OSError as error:
                    print(f"Connection error: {error}")

    except KeyboardInterrupt:
        print("\nServer stopped by user.")

    except OSError as error:
        print(f"Socket error: {error}")

    finally:
        if server is not None:
            server.close()
        print("Server socket closed.")

if __name__ == "__main__":
    start_server()
