# 🎮 Test Your Chat App NOW!

Both servers are already running! Choose your test:

---

## 🚀 Option 1: Test CLI Version (30 seconds)

### Open a NEW terminal and paste this:

```bash
python beginner_cli/client.py
```

### Then open ANOTHER terminal and paste this:

```bash
python beginner_cli/client.py
```

### Now type in either terminal:
```
Hello from terminal 1!
```

**You'll see it appear in BOTH terminals!** ✨

Type `exit` to quit.

---

## 🎨 Option 2: Test GUI Version (2 minutes)

### Open a NEW terminal and paste this:

```bash
python advanced_gui/main.py
```

### A window will appear! Follow these steps:

1. **Click "Register"**
2. **Fill in:**
   - Username: `alice`
   - Email: `alice@test.com` (optional)
   - Password: `password123`
   - Confirm: `password123`
3. **Click "Register"** button
4. **After success, login:**
   - Username: `alice`
   - Password: `password123`
5. **Click "Login"**
6. **In the chat window:**
   - Click "General" room on the left
   - Type "Hello World!" in the text box
   - Click "Send" or press Enter
7. **Try the emoji button (😀)** - Click it and select an emoji!
8. **Try the attachment button (📎)** - Select an image file!

---

## 🎯 Test with 2 Users (Advanced)

### Terminal 1:
```bash
python advanced_gui/main.py
```
- Register as `alice` / `password123`
- Login and join "General" room

### Terminal 2:
```bash
python advanced_gui/main.py
```
- Register as `bob` / `password123`
- Login and join "General" room

### Now chat between alice and bob! 💬

---

## 📸 What You'll See

### CLI Version:
```
[CONNECTED] Connected to chat server at 127.0.0.1:5555
Type your messages and press Enter to send.
Type 'exit' to quit.

Hello from terminal 1!
[127.0.0.1:54321] Hello from terminal 2!
```

### GUI Version:
```
┌─────────────────────────────────────────┐
│  Chat App - alice                       │
├──────────┬──────────────────────────────┤
│ Rooms    │  # General                   │
│          │                              │
│ General  │  [10:30] alice: Hello World! │
│ Projects │  [10:31] bob: Hi Alice! 👋   │
│ Friends  │  [10:32] alice: 😀 Nice!     │
│          │                              │
│          │  ┌────────────────────────┐  │
│          │  │ Type your message...   │  │
│          │  └────────────────────────┘  │
│          │  [😀] [📎] [Send]            │
└──────────┴──────────────────────────────┘
```

---

## ✅ Features to Test

### CLI Version:
- [ ] Multiple clients connect
- [ ] Messages broadcast to all
- [ ] Exit command works

### GUI Version:
- [ ] User registration
- [ ] User login
- [ ] Room selection
- [ ] Send text messages
- [ ] Emoji picker
- [ ] File attachment
- [ ] Message history
- [ ] Multiple users chatting

---

## 🛑 When Done Testing

Press `Ctrl+C` in the terminal where servers are running, or just close the terminals.

---

## 🎉 That's It!

You now have a fully functional chat application!

**Enjoy! 💬✨**
