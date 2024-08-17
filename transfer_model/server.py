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
        client_socket.sendall(b'ACK')
        received_uuid = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.sendall(b'ACK')
        UUIDS = load_uuids()

        if received_uuid in UUIDS:
            file_name = UUIDS[received_uuid]['Filename']
            temp_file_path = os.path.join(TEMP_FOLDER, file_name)

            if os.path.exists(temp_file_path):
                client_socket.sendall(file_name.encode())
                client_socket.recv(BUFFER_SIZE)  # Wait for acknowledgment

                with open(temp_file_path, 'rb') as file:
                    while True:
                        bytes_read = file.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        client_socket.sendall(bytes_read)
                client_socket.sendall(b'<EOF>')

                client_socket.recv(BUFFER_SIZE) # Wait for acknowledgement

                # Remove the temporary file after sending
                if UUIDS[received_uuid]['Permanent'] == "False":
                    os.remove(temp_file_path)
                    del UUIDS[received_uuid]
                    save_uuids(UUIDS)
            else:
                client_socket.sendall(b'File not found')
        else:
            client_socket.sendall(b'UUID not found')
    finally:
        print(f"Sent file {file_name} to receiver with UUID {received_uuid}")
        client_socket.close()

def handle_sender(client_socket):
    try:
        client_socket.sendall(b'ACK')
        sender_uuid = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.sendall(b'ACK')
        file_name = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.sendall(b'ACK')
        file_size = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.sendall(b'ACK')
        permanent = client_socket.recv(BUFFER_SIZE).decode()

        UUIDS = load_uuids()

        UUIDS[sender_uuid] = {'Filename': file_name, 'Permanent': permanent}
        save_uuids(UUIDS)

        temp_file_path = os.path.join(TEMP_FOLDER, file_name)

        client_socket.sendall(b'Ready for file')

        file = open(temp_file_path, "wb")
        file_bytes = b''
        done = False

        while not done:
            data = client_socket.recv(BUFFER_SIZE)
            file_bytes += data

            if file_bytes[-5:] == b'<EOF>':
                done = True
                file_bytes = file_bytes[:-5]
        
        file.write(file_bytes)
        file.close()
    
        client_socket.sendall(b'File received')

    finally:
        print(f"Received file {file_name} from sender with UUID {sender_uuid}")
        client_socket.close()

def handle_checkAlive(client_socket):
    client_socket.sendall(b'TransferX Server ACK')
    client_socket.close()

def handle_dbQuery(client_socket):
    client_socket.sendall(json.dumps(load_uuids()).encode())
    client_socket.close()

def handle_delete(client_socket):
    client_socket.sendall(b'ACK')
    UUID = client_socket.recv(BUFFER_SIZE).decode()

    UUIDS = load_uuids()
    if UUID in UUIDS:
        filename = UUIDS[UUID]['Filename']
        os.remove(os.path.join('temp_files', filename))
        del UUIDS[UUID]
        save_uuids(UUIDS)
    else:
        print(UUID)
    
    client_socket.close()
    print(f"{filename} has been deleted manually.")

if __name__ == "__main__":
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', SERVER_PORT))
        server_socket.listen()
        print(f"Server is listening on port {SERVER_PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            client_type = client_socket.recv(BUFFER_SIZE).decode()

            if client_type == 'sender':
                threading.Thread(target=handle_sender, args=(client_socket,)).start()
            elif client_type == 'receiver':
                threading.Thread(target=handle_client, args=(client_socket,)).start()
            elif client_type == 'checker':
                threading.Thread(target=handle_checkAlive, args=(client_socket,)).start()
            elif client_type == 'dbdataquery':
                threading.Thread(target=handle_dbQuery, args=(client_socket,)).start()
            elif client_type == 'delete':
                threading.Thread(target=handle_delete, args=(client_socket,)).start()
            else:
                print(f"Unknown client type: {client_type}")
                client_socket.close()
