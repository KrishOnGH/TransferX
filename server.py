import socket
import threading
import os
import json

# Constants
BUFFER_SIZE = 4096
UUIDS_FILE = 'uuids.json'
SERVER_PORT = 65432

def load_uuids():
    if os.path.exists(UUIDS_FILE):
        with open(UUIDS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_uuids(uuids):
    with open(UUIDS_FILE, 'w') as f:
        json.dump(uuids, f)

UUIDS = load_uuids()

def handle_client(client_socket):
    try:
        print("Receiver client connected")
        received_uuid = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Current UUIDS: {UUIDS}")
        print(f"Received UUID: {received_uuid}")

        if received_uuid in UUIDS:
            file_name = UUIDS[received_uuid]
            client_socket.sendall(b'Success')
            with open(file_name, 'rb') as file:
                while chunk := file.read(BUFFER_SIZE):
                    client_socket.sendall(chunk)
            print(f"Sent file {file_name}")
        else:
            client_socket.sendall(b'UUID not found')
    finally:
        client_socket.close()

def handle_sender(client_socket):
    global UUIDS
    try:
        print("Sender client connected")
        sender_uuid = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Received sender UUID: {sender_uuid}")
        file_name = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Received file name: {file_name}")

        UUIDS[sender_uuid] = file_name
        save_uuids(UUIDS)
        
        client_socket.sendall(b'Ready for file')
        
        with open(file_name, 'wb') as file:
            while True:
                chunk = client_socket.recv(BUFFER_SIZE)
                if not chunk:
                    break
                file.write(chunk)
        
        print(f"Received file {file_name} from sender with UUID {sender_uuid}")
        client_socket.sendall(b'File received')
    finally:
        client_socket.close()

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', SERVER_PORT))
        server_socket.listen()
        print(f"Server is listening on port {SERVER_PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"New connection from {addr}")
            client_type = client_socket.recv(BUFFER_SIZE).decode()
            print(f"Received client type: {client_type}")
            if client_type == 'sender':
                threading.Thread(target=handle_sender, args=(client_socket,)).start()
            elif client_type == 'receiver':
                threading.Thread(target=handle_client, args=(client_socket,)).start()
            else:
                print(f"Unknown client type: {client_type}")
                client_socket.close()