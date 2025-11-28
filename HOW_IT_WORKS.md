# 🔍 How the Chat Application Works

## 📖 Complete Step-by-Step Explanation

---

## 🎯 Overview: The Big Picture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   sandy's   │         │             │         │   alice's   │
│   Computer  │◄───────►│   SERVER    │◄───────►│   Computer  │
│  (Client)   │         │  (Port 5556)│         │  (Client)   │
└─────────────┘         └──────┬──────┘         └─────────────┘
                               │
                        ┌──────▼──────┐
                        │  DATABASE   │
                        │  (SQLite)   │
                        └─────────────┘
```

---

## 🚀 Part 1: Starting the Application

### Step 1: Start the Server

```bash
python advanced_gui/core/network.py
```

**What Happens:**
```python
1. Server creates a TCP socket
2. Binds to 127.0.0.1:5556 (localhost, port 5556)
3. Starts listening for connections
4. Waits for clients to connect
```

**Server Output:**
```
[STARTING] Chat server on 127.0.0.1:5556
[LISTENING] Waiting for connections...
```

---

### Step 2: Start the Client (GUI)

```bash
python advanced_gui/main.py
```

**What Happens:**
```python
1. Opens login window (Tkinter GUI)
2. Waits for user to login or register
```

---

## 👤 Part 2: User Registration & Login

### Registration Flow

**You click "Register" and enter:**
- Username: `sandy`
- Email: `sandy@example.com`
- Password: `mypassword`

**What Happens Behind the Scenes:**

```python
# 1. In register_window.py
def handle_register():
    username = "sandy"
    password = "mypassword"
    
    # 2. Call auth.register_user()
    auth.register_user(username, email, password)

# 3. In auth.py
def register_user(username, email, password):
    # Hash the password with bcrypt
    salt = bcrypt.gensalt()  # Random salt: $2b$12$xyz...
    password_hash = bcrypt.hashpw(password, salt)
    # Result: $2b$12$xyz...abc (60 characters)
    
    # 4. Save to database
    db.create_user(username, email, password_hash)

# 5. In database.py
def create_user(username, email, password_hash):
    # SQL: INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)
    # Database now has:
    # id=1, username='sandy', password_hash='$2b$12$xyz...'
```

**Why Hash Passwords?**
```
Plain password: "mypassword"
                    ↓ (bcrypt with salt)
Hashed: "$2b$12$xyz...abc"

Even if someone steals the database, they can't get your password!
```

---

### Login Flow

**You enter:**
- Username: `sandy`
- Password: `mypassword`

**What Happens:**

```python
# 1. In login_window.py
def handle_login():
    username = "sandy"
    password = "mypassword"
    
    # 2. Call auth.login_user()
    success, user, message = auth.login_user(username, password)

# 3. In auth.py
def login_user(username, password):
    # Get user from database
    user = db.get_user_by_username("sandy")
    # user.password_hash = "$2b$12$xyz...abc"
    
    # Verify password
    if bcrypt.checkpw(password, user.password_hash):
        return True, user, "Login successful"
    else:
        return False, None, "Invalid password"

# 4. If successful, open chat window
chat_window = ChatWindow(user)
```

---

## 🔌 Part 3: Connecting to Server

**After login, chat window opens:**

```python
# In chat_window.py - __init__()
def __init__(self, user):
    self.user = user  # User object (id=1, username='sandy')
    self.create_widgets()  # Create GUI
    self.connect_to_server()  # Connect to server

# connect_to_server()
def connect_to_server():
    # 1. Create TCP socket
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Connect to server
    self.socket.connect(('127.0.0.1', 5556))
    # Now connected!
    
    # 3. Start background thread to receive messages
    receive_thread = threading.Thread(target=self.receive_messages)
    receive_thread.daemon = True
    receive_thread.start()
    
    # 4. Send login message to server
    login_msg = {
        'action': 'LOGIN',
        'username': 'sandy',
        'user_id': 1
    }
    self.socket.send(json.dumps(login_msg) + '\n')
    
    # 5. Request list of rooms
    self.request_rooms()
```

**Server Side:**

```python
# In network.py - handle_client()
def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected")
    
    # Receive login message
    data = client_socket.recv(4096)
    message = json.loads(data)
    # message = {'action': 'LOGIN', 'username': 'sandy', 'user_id': 1}
    
    # Store client info
    clients[client_socket] = {
        'user_id': 1,
        'username': 'sandy',
        'room_id': None
    }
```

---

## 🏠 Part 4: Loading Rooms

**Client requests rooms:**

```python
# In chat_window.py
def request_rooms():
    msg = {'action': 'GET_ROOMS'}
    self.socket.send(json.dumps(msg) + '\n')
```

**Server responds:**

```python
# In network.py
def handle_get_rooms(client_socket):
    # Get rooms from database
    rooms = db.get_all_rooms()
    # rooms = [
    #   {'id': 1, 'name': 'General', 'description': '...'},
    #   {'id': 2, 'name': 'Projects', 'description': '...'},
    #   {'id': 3, 'name': 'Friends', 'description': '...'}
    # ]
    
    # Send back to client
    send_to_client(client_socket, {
        'action': 'SUCCESS',
        'rooms': rooms
    })
```

**Client displays rooms:**

```python
# In chat_window.py - receive_messages()
if action == 'SUCCESS' and 'rooms' in message:
    # Update room panel on main thread
    self.after(0, lambda: self.room_panel.update_rooms(message['rooms']))

# In room_list_panel.py
def update_rooms(rooms):
    # Create button for each room
    for room in rooms:
        btn = tk.Button(text=room['name'], command=lambda r=room: self.select_room(r))
        btn.pack()
    
    # Now you see: General, Projects, Friends buttons!
```

---

## 💬 Part 5: Sending a Message

**You type "Hello everyone!" and click Send**

### Step 1: Encrypt Message

```python
# In chat_window.py - send_message()
content = "Hello everyone!"

# Encrypt with Fernet
encrypted = encryption.encrypt(content)
# Result: "gAAAAABh3x2yKL..." (base64 encoded)
```

**How Encryption Works:**
```
Plain text: "Hello everyone!"
              ↓ (Fernet encryption with secret key)
Encrypted: "gAAAAABh3x2yKL..."

Only someone with the same key can decrypt it!
```

### Step 2: Display Locally (Immediately)

```python
# Show in your own window right away
self.display_own_message(content, 'text')

# This adds to your chat display:
# [11:46] sandy: Hello everyone!
```

### Step 3: Send to Server

```python
msg = {
    'action': 'SEND_MESSAGE',
    'content': 'gAAAAABh3x2yKL...',  # encrypted
    'message_type': 'text'
}
self.socket.send(json.dumps(msg) + '\n')
```

### Step 4: Server Receives

```python
# In network.py - handle_send_message()
def handle_send_message(client_socket, message):
    # Get client info
    client_info = clients[client_socket]
    room_id = client_info['room_id']  # e.g., 3 (Friends room)
    user_id = client_info['user_id']  # 1
    username = client_info['username']  # 'sandy'
    
    # Decrypt message
    encrypted_content = message['content']
    content = encryption.decrypt(encrypted_content)
    # content = "Hello everyone!"
    
    # Save to database
    db.save_message(
        room_id=3,
        sender_id=1,
        content="Hello everyone!",
        message_type='text'
    )
    # Now in database:
    # id=1, room_id=3, sender_id=1, content='Hello everyone!', created_at='2024-01-15 11:46:00'
```

### Step 5: Server Broadcasts

```python
    # Re-encrypt for transmission
    encrypted = encryption.encrypt(content)
    
    # Broadcast to all clients in the same room
    broadcast_to_room(room_id=3, {
        'action': 'MESSAGE',
        'username': 'sandy',
        'content': encrypted,  # 'gAAAAABh3x2yKL...'
        'message_type': 'text',
        'timestamp': '2024-01-15T11:46:00'
    })
```

**Who Gets the Message?**
```python
# rooms = {
#   3: [sandy_socket, alice_socket, bob_socket]
# }

# Server sends to alice_socket and bob_socket
# (NOT back to sandy_socket - you already see it!)
```

### Step 6: Other Clients Receive

**On alice's computer:**

```python
# In chat_window.py - receive_messages()
data = socket.recv(4096)
message = json.loads(data)
# message = {
#   'action': 'MESSAGE',
#   'username': 'sandy',
#   'content': 'gAAAAABh3x2yKL...',
#   'timestamp': '2024-01-15T11:46:00'
# }

# Decrypt message
encrypted = message['content']
content = encryption.decrypt(encrypted)
# content = "Hello everyone!"

# Display in alice's window
self.after(0, lambda: self.display_message(message))
# alice sees: [11:46] sandy: Hello everyone!
```

---

## 🔄 Complete Message Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    SANDY SENDS MESSAGE                       │
└─────────────────────────────────────────────────────────────┘

1. sandy types: "Hello everyone!"
        ↓
2. Encrypt: "gAAAAABh3x2yKL..."
        ↓
3. Display locally: [11:46] sandy: Hello everyone!
        ↓
4. Send to server via socket
        ↓
┌───────────────────────────────────────────────────────────┐
│                        SERVER                              │
├───────────────────────────────────────────────────────────┤
│ 5. Receive encrypted message                              │
│ 6. Decrypt: "Hello everyone!"                             │
│ 7. Save to database (room_id=3, sender_id=1)             │
│ 8. Re-encrypt: "gAAAAABh3x2yKL..."                        │
│ 9. Broadcast to all in room 3 (except sandy)             │
└───────────────────────────────────────────────────────────┘
        ↓                           ↓
┌───────────────┐         ┌───────────────┐
│  alice's PC   │         │   bob's PC    │
├───────────────┤         ├───────────────┤
│ 10. Receive   │         │ 10. Receive   │
│ 11. Decrypt   │         │ 11. Decrypt   │
│ 12. Display:  │         │ 12. Display:  │
│ [11:46] sandy:│         │ [11:46] sandy:│
│ Hello everyone│         │ Hello everyone│
└───────────────┘         └───────────────┘
```

---

## 🔐 Security Features Explained

### 1. Password Hashing (bcrypt)

```python
# When you register:
password = "mypassword"
    ↓
salt = bcrypt.gensalt()  # Random: $2b$12$xyz...
    ↓
hash = bcrypt.hashpw(password, salt)
    ↓
stored = "$2b$12$xyz...abc"  # 60 characters

# When you login:
entered_password = "mypassword"
stored_hash = "$2b$12$xyz...abc"
    ↓
bcrypt.checkpw(entered_password, stored_hash)
    ↓
Returns True if match, False otherwise
```

**Why it's secure:**
- Each password has unique salt
- Slow by design (prevents brute force)
- Can't reverse the hash to get password

### 2. Message Encryption (Fernet)

```python
# Encryption:
plain = "Hello"
key = b'YourSecretKey...'  # 32 bytes
    ↓
encrypted = Fernet(key).encrypt(plain)
    ↓
result = "gAAAAABh3x2yKL..."

# Decryption:
encrypted = "gAAAAABh3x2yKL..."
key = b'YourSecretKey...'  # Same key!
    ↓
plain = Fernet(key).decrypt(encrypted)
    ↓
result = "Hello"
```

**Why it's secure:**
- Messages encrypted in transit
- Eavesdropper sees gibberish
- Only clients with key can decrypt

---

## 🎨 GUI Components Explained

### Main Chat Window Layout

```
┌─────────────────────────────────────────────────────┐
│  Chat App - sandy                    [_] [□] [X]    │  ← Title bar
├──────────────┬──────────────────────────────────────┤
│              │  # Friends                           │  ← Room title
│ Chat Rooms   ├──────────────────────────────────────┤
│              │  ┌────────────────────────────────┐  │
│  Friends ✓   │  │ [11:46] sandy: Hello!         │  │  ← Message display
│  General     │  │ [11:47] alice: Hi sandy!      │  │     (ScrolledText)
│  Projects    │  │ [11:48] sandy: How are you?   │  │
│              │  │                                │  │
│              │  └────────────────────────────────┘  │
│              │  ┌────────────────────────────────┐  │
│              │  │ Type your message here...      │  │  ← Message input
│              │  │                                │  │     (Text widget)
│              │  └────────────────────────────────┘  │
│              │  [😀] [📎] [Send]                   │  ← Buttons
└──────────────┴──────────────────────────────────────┘
```

### How GUI Updates Work

```python
# WRONG - Causes freeze:
def receive_messages():
    message = socket.recv()
    room_panel.update_rooms(rooms)  # Called from background thread!
    # ❌ Tkinter doesn't like this!

# CORRECT - Use main thread:
def receive_messages():
    message = socket.recv()
    self.after(0, lambda: room_panel.update_rooms(rooms))
    # ✅ Scheduled on main thread!
```

**Why?**
- Tkinter GUI must update on main thread only
- `after(0, ...)` schedules function to run on main thread
- Background threads can't touch GUI directly

---

## 🗄️ Database Structure

```sql
-- users table
┌────┬──────────┬───────────────────┬──────────────────┬────────────┐
│ id │ username │ email             │ password_hash    │ created_at │
├────┼──────────┼───────────────────┼──────────────────┼────────────┤
│ 1  │ sandy    │ sandy@example.com │ $2b$12$xyz...   │ 2024-01-15 │
│ 2  │ alice    │ alice@example.com │ $2b$12$abc...   │ 2024-01-15 │
└────┴──────────┴───────────────────┴──────────────────┴────────────┘

-- rooms table
┌────┬──────────┬─────────────────────────┬────────────┐
│ id │ name     │ description             │ created_at │
├────┼──────────┼─────────────────────────┼────────────┤
│ 1  │ General  │ General discussion room │ 2024-01-15 │
│ 2  │ Projects │ Project discussions     │ 2024-01-15 │
│ 3  │ Friends  │ Casual chat             │ 2024-01-15 │
└────┴──────────┴─────────────────────────┴────────────┘

-- messages table
┌────┬─────────┬───────────┬──────────────────┬──────────────┬────────────┐
│ id │ room_id │ sender_id │ content          │ message_type │ created_at │
├────┼─────────┼───────────┼──────────────────┼──────────────┼────────────┤
│ 1  │ 3       │ 1         │ Hello everyone!  │ text         │ 11:46:00   │
│ 2  │ 3       │ 2         │ Hi sandy!        │ text         │ 11:47:00   │
│ 3  │ 1       │ 1         │ Anyone here?     │ text         │ 11:50:00   │
└────┴─────────┴───────────┴──────────────────┴──────────────┴────────────┘
```

---

## 🎯 Summary: The Complete Flow

1. **Start Server** → Listens on port 5556
2. **Start Client** → Opens login window
3. **Register/Login** → Password hashed, user authenticated
4. **Connect to Server** → Socket connection established
5. **Load Rooms** → Server sends room list, client displays buttons
6. **Select Room** → Client joins room on server
7. **Send Message** → Encrypt → Display locally → Send to server
8. **Server Processes** → Decrypt → Save to DB → Re-encrypt → Broadcast
9. **Other Clients Receive** → Decrypt → Display
10. **Everyone Sees Message** → Real-time chat! 🎉

---

**That's how your chat application works from start to finish!** 🚀
