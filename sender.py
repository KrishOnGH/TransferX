import socket
import os

# Constants
UUID = '1234'
BUFFER_SIZE = 4096
IP = '127.0.0.1'
SERVER_PORT = 65432

def send_file(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, SERVER_PORT))
        print("Connected to server")

        s.sendall(b'sender')
        s.recv(BUFFER_SIZE)  # Wait for acknowledgment
        s.sendall(str(UUID).encode())
        
        file_name = os.path.basename(file_path)
        s.sendall(file_name.encode())
        
        response = s.recv(BUFFER_SIZE).decode()
        if response == 'Ready for file':
            print(f"Sending file: {file_name}")
            with open(file_path, 'rb') as file:
                while chunk := file.read(BUFFER_SIZE):
                    s.sendall(chunk)
            s.sendall(b'EOF')  # Send EOF marker
            print(f"File {file_name} sent successfully")
            
            response = s.recv(BUFFER_SIZE).decode()
            print(f"Server response: {response}")
        else:
            print(f"Unexpected server response: {response}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'folder', 'file.txt')
    send_file(file_path)