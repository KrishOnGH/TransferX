import socket
import os

# Constants
UUID = '540639'
BUFFER_SIZE = 4096
IP = '192.168.29.80'
SERVER_PORT = 65432

def receive_file(Server, UUID, folder_path, encryption_key, signature):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((Server['IP'], Server['Port']))

        s.sendall(b'receiver')
        s.recv(BUFFER_SIZE)  # Wait for acknowledgment

        s.sendall(str(signature).encode())
        s.recv(BUFFER_SIZE) # Wait for acknowledgement

        s.sendall(str(UUID).encode())
        s.recv(BUFFER_SIZE)  # Wait for acknowledgment

        response = s.recv(BUFFER_SIZE).decode()
        if response != 'UUID not found' and response != 'File not found':
            file_name = response
            file_name = file_name[:-8]
            base_file_name = file_name
            file_name_is_available = False
            name_check_iteration = 0

            while not file_name_is_available:
                if os.path.exists(os.path.join(folder_path, file_name)):
                    name_check_iteration += 1
                    file_name = str(base_file_name.split(".")[0]) + ' (' + str(name_check_iteration) + ')' + '.' + str('.'.join(base_file_name.split('.')[1:]))
                else:
                    file_name_is_available = True

            s.sendall(b'Ready to receive')

            key_bytes = encryption_key.to_bytes((encryption_key.bit_length() + 7) // 8, byteorder='big')

            file = open(os.path.join(folder_path, file_name), "wb")
            file_bytes = b''
            done = False
            key_index = 0

            while not done:
                data = s.recv(BUFFER_SIZE)
                file_bytes += data

                if file_bytes[-5:] == b'<EOF>':
                    done = True
                    file_bytes = file_bytes[:-5]

            # Decrypt the received data
            decrypted_bytes = bytes(b ^ key_bytes[key_index % len(key_bytes)] for key_index, b in enumerate(file_bytes))

            file.write(decrypted_bytes)
            file.close()

            s.sendall(b'complete')
            return({"message": "success"})
        
        else:
            return({"message": "error", 'details': 'Incorrect UUID'})
        