import socket
import library
import logging
import time
import threading
from threading import Lock

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Server has started")

des_key_lock = Lock()


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


def update_des_key_periodically():
    global des_key
    while True:
        time.sleep(60)  # Wait 60 seconds before updating the key
        with des_key_lock:
            des_key = int(time.time()) % 1024  # Regenerate a new DES key
            print(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] DES Key updated to: {bin(des_key)[2:]}"
            )


# Handle receiving and decrypting messages
def receive_message(conn):
    data = conn.recv(1024).decode()
    if not data:
        return None
    time.sleep(3)
    print(f"Received from client: {data}")
    decrypted_message = library.decrypt(data)
    print(f"Decrypted Message: {decrypted_message}")
    return decrypted_message


# Inside the main server loop, ensure key change is delayed until after message transmission
def send_message_with_key_check(conn):
    while True:
        decrypted_message = receive_message(conn)
        if decrypted_message is None:
            break  # Exit loop if client disconnects or sends nothing

        with des_key_lock:  # Ensure key is not updated during message sending
            """
            Send message & encrypt the message
            """
            while True:
                message = input("#server -> ")
                if validate_input(message):
                    logging.info(f"Input received: {message}")
                    finalEncryptedMessage = library.encrypt(message)
                    print("Encrypted message =", finalEncryptedMessage)

                    library.sending()
                    conn.send(finalEncryptedMessage.encode())
                    break
                else:
                    logging.error("Invalid input, please try again.\n")


valid_credentials = {"root": "root", "riyanda": "tc22"}


def validate_credentials(username, password):
    return valid_credentials.get(username) == password


def validate_input(user_input):
    if not user_input:
        logging.warning("Input can't be empty.")
        return False
    return True


def main():
    global des_key
    des_key = 123  # Initial DES key

    # Start DES key update thread
    # Start DES key update thread
    threading.Thread(target=update_des_key_periodically, daemon=True).start()

    host = "127.0.0.1"
    port = 7000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server is running...")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Request client's public key from PKA
    client_public_key = get_public_key_from_pka("client")

    # Receive DES key handshake
    encrypted_des_key = int(conn.recv(1024).decode())
    des_key = rsa_decrypt(encrypted_des_key, (413, 3233))  # Server's private key
    print(f"Handshake completed. Received DES Key: {bin(des_key)[2:]}")
    conn.send("ACK".encode())  # Send acknowledgment

    while True:
        conn.send("Enter your username: ".encode())
        username = conn.recv(1024).decode()
        conn.send("Enter your password: ".encode())
        password = conn.recv(1024).decode()

        logging.info(f"Username: {username}, Password: {password}")

        if validate_credentials(username, password):
            logging.info("User authenticated successfully.")
            conn.send("Authentication successful.".encode())
            break
        else:
            logging.warning("Authentication failed.")
            conn.send("Authentication failed. Please try again.".encode())
            # Close the connection properly when authentication fails
            conn.close()
            return  # Exit after authentication failure

    # Now using send_message_with_key_check to handle sending encrypted messages
    send_message_with_key_check(conn)

    conn.close()


if __name__ == "__main__":
    main()
