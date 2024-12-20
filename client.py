import socket
import library
import logging
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Client has started")


def validate_input(user_input):
    if not user_input:
        logging.warning("Input cannot be empty")
        return False
    return True


# RSA Implementation
def rsa_encrypt(message, key):
    e, n = key
    return pow(message, e, n)


def rsa_decrypt(ciphertext, key):
    d, n = key
    return pow(ciphertext, d, n)


def get_public_key_from_pka(identity):
    pka_host = "127.0.0.1"
    pka_port = 6000
    with socket.socket() as pka_socket:
        pka_socket.connect((pka_host, pka_port))
        timestamp = str(time.time())
        pka_socket.send(f"{identity} {timestamp}".encode())
        response = pka_socket.recv(1024).decode()
        return tuple(map(int, response.split()))


def send_message(mySocket, message):
    # Send the message followed by a newline or other delimiter
    mySocket.send(message.encode() + b"\n")  # Send a newline to signify the end


def authenticate(mySocket):
    while True:
        username_prompt = mySocket.recv(1024).decode()
        print(username_prompt)
        username = input("Your username: ")
        mySocket.send(username.encode())

        password_prompt = mySocket.recv(1024).decode()
        print(password_prompt)
        password = input("Your password: ")
        mySocket.send(password.encode())

        response = mySocket.recv(1024).decode().strip()
        print(f"Server response: {response}")

        if response == "Authentication successful.":
            break
        elif response == "Authentication failed. Please try again.":
            print("Authentication failed. Please try again.")
            break  # Exit the loop after a failed attempt


def main():
    server_host = "127.0.0.1"
    server_port = 7000

    # Connect to server
    client_socket = socket.socket()
    client_socket.connect((server_host, server_port))

    # Request server's public key from PKA
    server_public_key = get_public_key_from_pka("server")

    # Handshake: Send encrypted DES key
    des_key = int("1001100111", 2)
    encrypted_des_key = rsa_encrypt(des_key, server_public_key)
    client_socket.send(str(encrypted_des_key).encode())

    # Wait for server acknowledgment (optional)
    ack = client_socket.recv(1024).decode()
    if ack != "ACK":
        print("Handshake failed. Closing connection.")
        client_socket.close()
        return

    # DES Key Debugging
    print(f"Using DES Key: {bin(des_key)[2:]}")

    # Authenticate with server
    authenticate(client_socket)

    message = input("#client -> ")

    while message != "q":
        if validate_input(message):
            logging.info(f"Input received: {message}")
            finalEncryptedMessage = library.encrypt(message)
            client_socket.send(finalEncryptedMessage.encode())
            print("Encrypted message = " + finalEncryptedMessage)
            library.sending()

            data = client_socket.recv(1024).decode()
            print("Received from server = " + data)

            decryptedMessage = library.decrypt(data)
            if not data:
                break
            print("Decrypted Message = " + str(decryptedMessage))
        else:
            logging.error("Invalid input, please try again.")

        message = input("Enter the message you want to encrypt -> ")

    client_socket.close()


if __name__ == "__main__":
    main()
