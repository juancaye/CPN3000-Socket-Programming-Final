
import socket
import ssl

# Configure the server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12001
BUFFER_SIZE = 1024

# Create TLS client
def start_client():
    client = None
    secure_client = None

    try:
        # Trust the self-signed server certificate
        context = ssl.create_default_context(
            ssl.Purpose.SERVER_AUTH
        )
        context.load_verify_locations(
            cafile="server.crt"
        )

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)

        # Get user input
        message = input("Enter a message: ").strip()

        if not message:
            print("Error: Message cannot be empty.")
            return

        # Convert message to bytes
        data = message.encode("utf-8")

        if len(data) > BUFFER_SIZE:
            print("Error: Message is too long.")
            return

        # Establish TCP connection, then upgrade to TLS
        client.connect((SERVER_IP, SERVER_PORT))
        secure_client = context.wrap_socket(
            client,
            server_hostname="localhost"
        )
        print("Connected securely to TLS server.")
        print(f"TLS version: {secure_client.version()}")

        # Send message
        secure_client.sendall(data)
        print("Message sent to server.")

        # Receive server response
        response = secure_client.recv(BUFFER_SIZE)

        if not response:
            print("Error: Server closed the connection.")
            return

        print(f"Server replied: {response.decode('utf-8')}")

    except ssl.SSLError as error:
        print(f"TLS error: {error}")

    except socket.timeout:
        print("Error: Connection or communication timed out.")

    except ConnectionRefusedError:
        print("Error: Server is not running or refused the connection.")

    except UnicodeError:
        print("Error: Invalid message encoding.")

    except KeyboardInterrupt:
        print("\nClient stopped by user.")

    except OSError as error:
        print(f"Socket error: {error}")

    finally:
        if secure_client is not None:
            secure_client.close()
        elif client is not None:
            client.close()
        print("Client socket closed.")

if __name__ == "__main__":
    start_client()
