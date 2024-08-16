import socket
import os

# Constaints
UUID = '1234'
BUFFER_SIZE = 4096
IP = '127.0.0.1'
SERVER_PORT = 65432

def send_file(Server, UUID, file_path):
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
        s.sendall(file_name.encode())
        s.sendall(str(file_size).encode())
        
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

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'folder', 'file.txt')
    print(send_file({"IP": IP, "Port": SERVER_PORT}, UUID, file_path))
