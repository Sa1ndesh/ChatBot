# Quick Start Guide

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Beginner CLI Version

### Step 1: Start the Server
Open a terminal and run:
```bash
python beginner_cli/server.py
```

You should see:
```
[STARTING] Server is starting on 127.0.0.1:5555
[LISTENING] Server is listening for connections...
```

### Step 2: Start Clients
Open 2-3 additional terminals and run in each:
```bash
python beginner_cli/client.py
```

### Step 3: Chat!
- Type messages in any client and press Enter
- Messages will appear in all other clients
- Type 'exit' to disconnect

## Advanced GUI Version

### Step 1: Start the Server
Open a terminal and run:
```bash
python advanced_gui/core/network.py
```

You should see:
```
[STARTING] Chat server on 127.0.0.1:5556
[LISTENING] Waiting for connections...
```

### Step 2: Start the Application
Open another terminal and run:
```bash
python advanced_gui/main.py
```

### Step 3: Register an Account
1. Click "Register" button
2. Enter username (min 3 characters)
3. Enter email (optional)
4. Enter password (min 6 characters)
5. Confirm password
6. Click "Register"

### Step 4: Login
1. Enter your username and password
2. Click "Login"

### Step 5: Start Chatting!
1. Select a room from the left panel (General, Projects, or Friends)
2. Type your message in the text box at the bottom
3. Click "Send" or press Enter
4. Use the emoji button (😀) to add emojis
5. Use the attachment button (📎) to share images

## Testing with Multiple Users

To test the chat with multiple users:

1. Keep the server running
2. Run `python advanced_gui/main.py` in multiple terminals
3. Register different accounts in each window
4. Join the same room and start chatting!

## Features to Try

- **Multiple Rooms**: Switch between General, Projects, and Friends rooms
- **Emojis**: Click the emoji button to add emojis to your messages
- **Image Sharing**: Click the attachment button to share images
- **Message History**: Previous messages are loaded when you join a room
- **Encryption**: All messages are encrypted during transmission
- **Notifications**: Rooms with new messages are highlighted in red

## Troubleshooting

### "Connection refused" error
- Make sure the server is running first
- Check that the ports (5555 for CLI, 5556 for GUI) are not in use

### "Module not found" error
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Make sure you're running from the project root directory

### Database errors
- The database file `chat_app.db` will be created automatically
- If you encounter issues, delete `chat_app.db` and restart

### Import errors in advanced GUI
- Make sure you're running from the project root
- The code uses sys.path.append to handle imports

## Notes

- The beginner CLI version uses port 5555
- The advanced GUI version uses port 5556
- Both can run simultaneously
- The database file `chat_app.db` is created in the project root
- Uploaded files are stored in `advanced_gui/assets/uploads/`
