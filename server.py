import socket
import threading
import os
import json

# Constants
BUFFER_SIZE = 4096
UUIDS_FILE = 'uuids.json'
SERVER_PORT = 65432
TEMP_FOLDER = 'temp_files'

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
        client_socket.sendall(b'ACK')
        received_uuid = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Received UUID: {received_uuid}")

        if received_uuid in UUIDS:
            file_name = UUIDS[received_uuid]
            temp_file_path = os.path.join(TEMP_FOLDER, file_name)
            
            if os.path.exists(temp_file_path):
                client_socket.sendall(file_name.encode())
                client_socket.recv(BUFFER_SIZE)  # Wait for acknowledgment
                
                print(f"Sending file {file_name}")
                with open(temp_file_path, 'rb') as file:
                    while chunk := file.read(BUFFER_SIZE):
                        client_socket.sendall(chunk)
                client_socket.sendall(b'EOF')  # Send EOF marker
                print(f"Sent file {file_name}")
                
                # Remove the temporary file after sending
                os.remove(temp_file_path)
                print(f"Removed temporary file {temp_file_path}")
                del UUIDS[received_uuid]
                save_uuids(UUIDS)
            else:
                client_socket.sendall(b'File not found')
        else:
            client_socket.sendall(b'UUID not found')
    finally:
        client_socket.close()
        print("Receiver client disconnected")

def handle_sender(client_socket):
    try:
        print("Sender client connected")
        client_socket.sendall(b'ACK')
        sender_uuid = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Received sender UUID: {sender_uuid}")
        file_name = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Received file name: {file_name}")

        UUIDS[sender_uuid] = file_name
        save_uuids(UUIDS)
        
        temp_file_path = os.path.join(TEMP_FOLDER, file_name)
        
        client_socket.sendall(b'Ready for file')
        
        print(f"Receiving file {file_name}")
        with open(temp_file_path, 'wb') as file:
            while True:
                chunk = client_socket.recv(BUFFER_SIZE)
                if chunk == b'EOF':
                    break
                file.write(chunk)
        
        print(f"Received file {file_name} from sender with UUID {sender_uuid}")
        client_socket.sendall(b'File received')
    finally:
        client_socket.close()
        print("Sender client disconnected")

if __name__ == "__main__":
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)
        print(f"Created temporary folder: {TEMP_FOLDER}")

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