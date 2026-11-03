
import socket
import ssl

# Configure the server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12000
BUFFER_SIZE = 1024

# Create UDP socket
def start_server():
    server = None

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.settimeout(1)

        # Bind the socket
        server.bind((SERVER_IP, SERVER_PORT))
        print("UDP server is running...")

        # Receive and return messages
        while True:
            try:
                data, client_address = server.recvfrom(BUFFER_SIZE)
            except socket.timeout:
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

            # Echo the message back to the client
            server.sendto(data, client_address)

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
