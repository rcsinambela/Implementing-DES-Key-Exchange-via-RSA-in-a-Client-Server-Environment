import socket
import library
import logging
import time
import threading

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Server has started")


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


def update_des_key_periodically(conn):
    global des_key
    while True:
        des_key = int(time.time()) % 1024  # Contoh regenerasi DES key
        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] DES Key updated to: {bin(des_key)[2:]}"
        )
        conn.send(f"KEY_UPDATE {bin(des_key)[2:]}".encode())  # Kirim key baru ke client
        time.sleep(60)  # Tunggu 60 detik sebelum memperbarui lagi


valid_credentials = {"daniel": "tc20", "riyanda": "tc22"}


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

    host = "127.0.0.1"
    port = 5000

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
    if not encrypted_des_key:
        print("[ERROR] No DES key received from client.")
        conn.close()
        return
    des_key = rsa_decrypt(encrypted_des_key, (413, 3233))  # Server's private key
    print(f"Handshake completed. Received DES Key: {bin(des_key)[2:]}")
    conn.send("ACK".encode())  # Send acknowledgment
    print("[DEBUG] ACK sent to client after handshake.")

    # Start DES key update thread
    threading.Thread(target=update_des_key_periodically(conn), daemon=True).start()

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

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Received from client: {data}")

        decrypted_message = library.decrypt(data)
        print(f"Decrypted Message: {decrypted_message}")
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

    conn.close()


if __name__ == "__main__":
    main()
