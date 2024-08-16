import socket
import os

# Constants
UUID = '1234'
BUFFER_SIZE = 4096
IP = '192.168.29.80'
SERVER_PORT = 65432

def receive_file():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, SERVER_PORT))
        print("Connected to server")

        s.sendall(b'receiver')
        s.recv(BUFFER_SIZE)  # Wait for acknowledgment
        s.sendall(str(UUID).encode())
        
        response = s.recv(BUFFER_SIZE).decode()
        if response != 'UUID not found' and response != 'File not found':
            file_name = response
            s.sendall(b'Ready to receive')
            
            base_name, ext = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(file_name):
                file_name = f"{base_name}{counter}{ext}"
                counter += 1
            
            print(f"Receiving file: {file_name}")
            with open(file_name, 'wb') as file:
                while True:
                    chunk = s.recv(BUFFER_SIZE)
                    if chunk == b'EOF':
                        break
                    file.write(chunk)
            print(f"File received and saved as '{file_name}'")
        else:
            print(f"Server response: {response}")

if __name__ == "__main__":
    receive_file()