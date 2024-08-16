import socket
import os

# Constants
UUID = '540639'
BUFFER_SIZE = 4096
IP = '192.168.29.80'
SERVER_PORT = 65432

def receive_file(Server, UUID, folder_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((Server['IP'], Server['Port']))

        s.sendall(b'receiver')
        s.recv(BUFFER_SIZE)  # Wait for acknowledgment

        s.sendall(str(UUID).encode())
        s.recv(BUFFER_SIZE)  # Wait for acknowledgment

        response = s.recv(BUFFER_SIZE).decode()
        if response != 'UUID not found' and response != 'File not found':
            file_name = response
            s.sendall(b'Ready to receive')

            file = open(os.path.join(folder_path, file_name[:-8]), "wb")
            file_bytes = b''
            done = False

            while not done:
                data = s.recv(BUFFER_SIZE)
                file_bytes += data

                if file_bytes[-5:] == b'<EOF>':
                    done = True
                    file_bytes = file_bytes[:-5]

            file.write(file_bytes)
            file.close()

            s.sendall(b'complete')
            return({"message": "success"})

        else:
            return({"message": "error", 'details': 'Incorrect UUID'})