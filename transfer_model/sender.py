import socket
import os

# Constaints
UUID = '1234'
BUFFER_SIZE = 4096
IP = '127.0.0.1'
SERVER_PORT = 65432

def send_file(Server, UUID, file_path, permanent):
    if not os.path.isfile(file_path):
        return({"message": "error"})
    else:
        file_name = os.path.basename(file_path) + '(' + str(UUID) + ')'
        file_size = os.path.getsize(file_path)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((Server['IP'], Server['Port']))

        s.sendall(b'sender')
        s.recv(BUFFER_SIZE)  # Wait for acknowledgment

        s.sendall(str(UUID).encode())
        s.recv(BUFFER_SIZE)  # Wait for acknowledgment

        s.sendall(file_name.encode())
        s.recv(BUFFER_SIZE)  # Wait for acknowledgment

        s.sendall(str(file_size).encode())
        s.recv(BUFFER_SIZE)  # Wait for acknowledgment

        s.sendall(str(permanent).encode())

        response = s.recv(BUFFER_SIZE).decode()
        if response == 'Ready for file':
            with open(file_path, 'rb') as file:
                while True:
                    bytes_read = file.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    s.sendall(bytes_read)
            s.sendall(b'<EOF>')

            response = s.recv(BUFFER_SIZE).decode()
            return({"message": "success"})
        else:
            return({"message": "error"})