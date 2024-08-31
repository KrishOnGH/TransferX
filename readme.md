# TransferX

TransferX is a tool that allows users to easily transfer files between computers anywhere in the world. It works for both Mac and Windows (Mac support not guaranteed) if all dependencies are downloaded.

## Components

1. Server instance: Hosts a server drive
2. Client utility: Adds a file explorer option for easy file transfers

## Setup and Running

### Server Setup
```
cd transfer_model
python main.py
```

### Client Setup
```
python main.py
```

Running `main.py` on a client computer adds a file explorer option, which appears when you right-click, in the same area as "Open with VSC" would.

## Usage

### Downloading Files
1. Right-click on a folder in file explorer
2. Select TransferX
3. Enter the UUID of the stored file
4. The file will be downloaded to the selected folder if the UUID is valid

### Uploading Files
1. Right-click on a file in file explorer
2. Select TransferX
3. Choose whether the file is permanent or temporary
   - Permanent: File remains on the server after download
   - Temporary: File is deleted from the server after first download
4. Continue to receive the UUID for the uploaded file

## Settings

In the settings page, you can configure:
- IP and port of your server
- Encryption key (must match on both sending and receiving computers)
- Signature (your unique client ID)

## Database Management

In the database page, you can:
- View all items stored in your database and their information
- Delete items, including permanent ones

## Notes
- Ensure all dependencies are downloaded for proper functionality
- Mac support is not guaranteed