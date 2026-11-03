
import socket
import ssl

# Configure the server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12001
BUFFER_SIZE = 1024

# Create TLS server
def start_server():
    server = None

    try:
        # Create the TLS context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_cert_chain(
            certfile="server.crt",
            keyfile="server.key"
        )

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket
        server.bind((SERVER_IP, SERVER_PORT))
        server.listen(5)
        server.settimeout(1)

        print("TLS server is running...")

        # Accept incoming connections
        while True:
            try:
                connection, client_address = server.accept()
            except socket.timeout:
                continue

            print(f"Connected to: {client_address}")

            # Perform the TLS handshake
            try:
                secure_connection = context.wrap_socket(
                    connection,
                    server_side=True
                )
            except (ssl.SSLError, OSError) as error:
                print(f"TLS handshake failed: {error}")
                connection.close()
                continue

            # Handle client communication
            with secure_connection:
                secure_connection.settimeout(5)
                print(f"TLS version: {secure_connection.version()}")

                try:
                    data = secure_connection.recv(BUFFER_SIZE)

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
                    secure_connection.sendall(data)
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
