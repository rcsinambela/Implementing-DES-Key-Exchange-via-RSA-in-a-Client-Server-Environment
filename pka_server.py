import socket
import time

# Public Key Database
keys = {
    "client": (17, 3233),  # Public key (e, n)
    "server": (7, 3233),  # Public key (e, n)
}


def handle_client(conn):
    while True:
        request = conn.recv(1024).decode()
        if not request:
            break
        print(f"Request received: {request}")

        parts = request.split()
        if len(parts) != 2 or parts[0] not in keys:
            conn.send("Invalid request".encode())
            continue

        identity, timestamp = parts
        current_time = time.time()

        # Validate timestamp (within 5 seconds)
        if abs(current_time - float(timestamp)) > 5:
            conn.send("Timestamp invalid".encode())
            continue

        # Respond with public key
        public_key = keys[identity]
        conn.send(f"{public_key[0]} {public_key[1]}".encode())


def main():
    host = "127.0.0.1"
    port = 6000
    server = socket.socket()
    server.bind((host, port))
    server.listen(5)
    print("PKA Server is running...")

    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        handle_client(conn)
        conn.close()


if __name__ == "__main__":
    main()
