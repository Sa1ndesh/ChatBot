# 🚀 Run Instructions - Python Chat Application

## ✅ Current Status

**Both servers are already running!**

- ✓ CLI Server: Running on `127.0.0.1:5555`
- ✓ GUI Server: Running on `127.0.0.1:5556`
- ✓ Database: Initialized (`chat_app.db` created)
- ✓ All files: Created and verified

## 🎮 Quick Test - Choose Your Version

### Option A: Test Beginner CLI Version (Simplest)

**Step 1:** Open a NEW terminal and run:
```bash
python beginner_cli/client.py
```

**Step 2:** Open ANOTHER terminal and run:
```bash
python beginner_cli/client.py
```

**Step 3:** Type messages in either terminal and watch them appear in both!

**Step 4:** Type `exit` to disconnect.

---

### Option B: Test Advanced GUI Version (Full Features)

**Step 1:** Open a NEW terminal and run:
```bash
python advanced_gui/main.py
```

**Step 2:** In the login window that appears:
- Click **"Register"** button
- Enter username: `alice` (or any name)
- Enter email: `alice@test.com` (optional)
- Enter password: `password123` (min 6 chars)
- Confirm password: `password123`
- Click **"Register"**

**Step 3:** After registration success:
- Enter username: `alice`
- Enter password: `password123`
- Click **"Login"**

**Step 4:** In the chat window:
- Click on **"General"** room in the left panel
- Type a message in the text box at bottom
- Click **"Send"** or press Enter
- Try the emoji button (😀) to add emojis!
- Try the attachment button (📎) to share images!

**Step 5 (Optional):** Test with multiple users:
- Open ANOTHER terminal
- Run `python advanced_gui/main.py` again
- Register as `bob` with password `password123`
- Login and join the same room
- Chat between alice and bob!

---

## 🎯 What You'll See

### CLI Version
```
[CONNECTED] Connected to chat server at 127.0.0.1:5555
Type your messages and press Enter to send.
Type 'exit' to quit.

[127.0.0.1:54321] Hello from client 1!
[127.0.0.1:54322] Hi from client 2!
```

### GUI Version
```
┌─────────────────────────────────────────┐
│  Chat App - alice                       │
├──────────┬──────────────────────────────┤
│ Rooms    │  # General                   │
│          │                              │
│ General  │  [10:30] alice: Hello!       │
│ Projects │  [10:31] bob: Hi there!      │
│ Friends  │  [10:32] alice: 😀           │
│          │                              │
│          │  ┌────────────────────────┐  │
│          │  │ Type message...        │  │
│          │  └────────────────────────┘  │
│          │  [😀] [📎] [Send]            │
└──────────┴──────────────────────────────┘
```

---

## 🛑 Stop Servers

When you're done testing, stop the servers:

**In the terminal where you started this:**
```bash
# Press Ctrl+C to stop
```

Or use these commands:
```bash
# Stop CLI server (process ID 2)
taskkill /F /PID <process_id>

# Stop GUI server (process ID 3)
taskkill /F /PID <process_id>
```

---

## 🔧 Troubleshooting

### "Connection refused" error
- The servers are already running, so this shouldn't happen
- If it does, restart the server:
  ```bash
  python beginner_cli/server.py
  # OR
  python advanced_gui/core/network.py
  ```

### GUI doesn't open
- Make sure you have tkinter installed
- On Windows, it comes with Python
- Try: `python -m tkinter` to test

### Can't register user
- Username must be at least 3 characters
- Password must be at least 6 characters
- Username must be unique

### Messages not appearing
- Make sure you're in the same room
- Check that the server is running
- Try refreshing by switching rooms

---

## 📚 Features to Explore

### CLI Version
- [x] Multi-client chat
- [x] Real-time broadcasting
- [x] Exit command

### GUI Version
- [x] User registration & login
- [x] Multiple chat rooms
- [x] Message history
- [x] Emoji picker (60+ emojis)
- [x] Image file sharing
- [x] Encrypted messages
- [x] User join/leave notifications
- [x] Room highlighting for new messages

---

## 🎉 Enjoy Your Chat App!

You now have a fully functional real-time chat application with:
- ✅ Socket programming
- ✅ Multi-threading
- ✅ Database persistence
- ✅ User authentication
- ✅ Message encryption
- ✅ Beautiful GUI
- ✅ Emoji support

**Happy Chatting! 💬**
