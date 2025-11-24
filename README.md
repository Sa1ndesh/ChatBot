# Python Real-Time Chat Application

A complete chat system implementation in Python with two levels:
1. **Beginner**: Command-line chat using sockets
2. **Advanced**: GUI-based chat with authentication, rooms, media sharing, and encryption

## Features

### Beginner CLI Version
- Socket-based TCP communication
- Multiple simultaneous clients
- Real-time message broadcasting
- Graceful disconnect handling

### Advanced GUI Version
- Tkinter-based graphical interface
- User registration and login with password hashing
- Multiple chat rooms
- Message history persistence (SQLite)
- Image file sharing
- Emoji support
- Basic message encryption (Fernet)
- Desktop notifications for new messages

## Requirements

```
Python 3.7+
tkinter (usually included with Python)
bcrypt
cryptography
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Beginner CLI Version

1. Start the server:
```bash
python beginner_cli/server.py
```

2. Start one or more clients (in separate terminals):
```bash
python beginner_cli/client.py
```

3. Type messages and press Enter. Type 'exit' to quit.

### Advanced GUI Version

1. Start the server:
```bash
python advanced_gui/core/network.py
```

2. Run the application:
```bash
python advanced_gui/main.py
```

3. Register a new account or login
4. Join rooms and start chatting!

## Database Schema

### Users Table
- id (PRIMARY KEY)
- username (UNIQUE)
- email
- password_hash
- created_at

### Rooms Table
- id (PRIMARY KEY)
- name (UNIQUE)
- description
- created_at

### Messages Table
- id (PRIMARY KEY)
- room_id (FOREIGN KEY)
- sender_id (FOREIGN KEY)
- content
- message_type (text/image)
- file_path
- created_at

## Security Features

- **Password Hashing**: bcrypt for secure password storage
- **Message Encryption**: Fernet symmetric encryption for messages in transit
- **SQL Injection Protection**: Parameterized queries

## Project Structure

```
chat_app/
├── beginner_cli/
│   ├── server.py          # CLI server
│   └── client.py          # CLI client
└── advanced_gui/
    ├── main.py            # Application entry point
    ├── config.py          # Configuration constants
    ├── schema.sql         # Database schema
    ├── core/
    │   ├── network.py     # Server implementation
    │   ├── database.py    # Database operations
    │   ├── auth.py        # Authentication logic
    │   ├── encryption.py  # Encryption utilities
    │   └── models.py      # Data models
    ├── ui/
    │   ├── login_window.py
    │   ├── register_window.py
    │   ├── chat_window.py
    │   ├── room_list_panel.py
    │   └── emoji_picker.py
    └── assets/
        ├── emojis.json
        ├── images/
        └── uploads/       # User-uploaded files
```

## Limitations & Future Improvements

- Single shared encryption key (production would use per-user keys)
- No video chat support
- Basic file sharing (images only)
- Local SQLite database (could migrate to PostgreSQL)
- No message editing/deletion
- No user profiles or avatars

## License

MIT License - Feel free to use for learning purposes!
