import socket
import uuid
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
        
        s.sendall(str(UUID).encode())
        
        response = s.recv(BUFFER_SIZE).decode()
        if 'Success' in response:
            file_name = 'received_file.txt'
            with open(file_name, 'wb') as file:
                while chunk := s.recv(BUFFER_SIZE):
                    if not chunk:
                        break
                    file.write(chunk)
            print(f"File received and saved as '{file_name}'")
        else:
            print(f"Server response: {response}")

if __name__ == "__main__":
    receive_file()
