import socket
import threading
import os
import json
import shutil
import datetime
from dateutil import parser

# Constants
BUFFER_SIZE = 4096
UUIDS_FILE = 'uuids.json'
SERVER_DATA_FILE = 'serverdata.json'
TEMP_FOLDER = 'temp_files'
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
        client_socket.sendall(b'ACK')
        signature = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.sendall(b'ACK')
        received_uuid = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.sendall(b'ACK')
        UUIDS = load_uuids()

        if os.path.exists(SERVER_DATA_FILE):
            with open(SERVER_DATA_FILE, 'r') as f:
                server_data = json.load(f)
        else:
            server_data = {"Clients": {}}

        if signature in server_data['Clients']:
            user_data = server_data['Clients'][signature]
            user_data['Last Date Active'] = str(datetime.date.today())
        else:
            user_data = {
                'Last Date Active': str(datetime.date.today()),
                'Files Sent': 0,
                'Files Received': 0
            }

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
                
                user_data['Files Received'] += 1    
                server_data['Clients'][signature] = user_data
                with open(SERVER_DATA_FILE, 'w') as f:
                    json.dump(server_data, f, indent=4)

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
        signature = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.sendall(b'ACK')
        sender_uuid = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.sendall(b'ACK')
        file_name = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.sendall(b'ACK')
        file_size = client_socket.recv(BUFFER_SIZE).decode()
        client_socket.sendall(b'ACK')
        permanent = client_socket.recv(BUFFER_SIZE).decode()

        if os.path.exists(SERVER_DATA_FILE):
            with open(SERVER_DATA_FILE, 'r') as f:
                server_data = json.load(f)
        else:
            server_data = {"Clients": {}}

        if signature in server_data['Clients']:
            user_data = server_data['Clients'][signature]
            user_data['Last Date Active'] = str(datetime.date.today())
        else:
            server_data['Clients'][signature] = {
                'Last Date Active': str(datetime.date.today()),
                'Files Sent': 0,
                'Files Received': 0
            }

        UUIDS = load_uuids()

        UUIDS[sender_uuid] = {'Filename': file_name, 'Permanent': permanent, 'Date': str(datetime.date.today())}
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

        user_data['Files Sent'] += 1
        server_data['Clients'][signature] = user_data
        with open(SERVER_DATA_FILE, 'w') as f:
            json.dump(server_data, f, indent=4)

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

def handle_vitalsQuery(client_socket):
    if os.path.exists(SERVER_DATA_FILE):
        with open(SERVER_DATA_FILE, 'r') as f:
            server_data = json.load(f)
    else:
        server_data = {"Clients": {}}

    clients = server_data['Clients']
    numClients = len(clients)
    numActiveClients = 0

    for clientSignature in clients:
        client = clients[clientSignature]
        if datetime.date.today() - parser.parse(client["Last Date Active"]).date() <= datetime.timedelta(days=7):
            numActiveClients += 1

    UUIDS = load_uuids()
    numFiles = len(UUIDS)
    numRecentFiles = 0

    for uuid in UUIDS:
        date_stored = UUIDS[uuid]['Date']
        if datetime.date.today() - parser.parse(date_stored).date() <= datetime.timedelta(days=30):
            numRecentFiles += 1

    total, used, free = shutil.disk_usage(TEMP_FOLDER)

    used = used / (1024 ** 3)
    free = free / (1024 ** 3)
    
    client_socket.sendall(json.dumps({"Clients Connected": numClients, "Active Clients": numActiveClients, "Files Stored": numFiles, "Recent Files": numRecentFiles, "GB Used": used, "GB Remaining": free}).encode())

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
