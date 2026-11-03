
import socket
import ssl

# Configure the server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12001
BUFFER_SIZE = 1024

# Create TCP client
def start_client():
    client = None

    try:
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

        # Establish TCP connection
        client.connect((SERVER_IP, SERVER_PORT))
        print("Connected to TCP server.")

        # Send message
        client.sendall(data)
        print("Message sent to server.")

        # Receive server response
        response = client.recv(BUFFER_SIZE)

        if not response:
            print("Error: Server closed the connection.")
            return

        print(f"Server replied: {response.decode('utf-8')}")

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
        if client is not None:
            client.close()
        print("Client socket closed.")

if __name__ == "__main__":
    start_client()
