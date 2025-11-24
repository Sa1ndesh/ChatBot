# 🎨 GUI Testing Guide - Step by Step

## ✅ Pre-Test Verification

Run this first to verify everything is ready:
```bash
python test_gui.py
```

You should see:
```
✓ Core modules imported successfully
✓ Database initialized
✓ Found 3 rooms:
  - Friends: Casual chat with friends
  - General: General discussion room
  - Projects: Project-related discussions
✓ Test user created
✓ Login successful for user: testuser
```

---

## 🚀 Step-by-Step GUI Test

### Step 1: Start the GUI Application

```bash
python advanced_gui/main.py
```

**What you should see:**
- A login window appears with title "Chat App - Login"
- Two input fields: Username and Password
- Two buttons: "Login" and "Register"

---

### Step 2: Register a New User

1. **Click the "Register" button**
2. **A new window appears: "Create New Account"**
3. **Fill in the form:**
   - Username: `alice` (minimum 3 characters)
   - Email: `alice@test.com` (optional)
   - Password: `password123` (minimum 6 characters)
   - Confirm: `password123` (must match)
4. **Click "Register"**
5. **You should see:** "Registration successful! You can now login."
6. **Click "OK"**

---

### Step 3: Login

1. **Back at the login window, enter:**
   - Username: `alice`
   - Password: `password123`
2. **Click "Login"**

**What you should see:**
- Login window closes
- Main chat window opens with title "Chat App - alice"

---

### Step 4: Verify Room List (LEFT SIDE)

**On the LEFT side of the chat window, you should see:**

```
┌──────────────┐
│ Chat Rooms   │
├──────────────┤
│  General     │  ← Clickable button
│  Projects    │  ← Clickable button
│  Friends     │  ← Clickable button
└──────────────┘
```

**Room buttons should:**
- Have a dark gray background (#34495e)
- Show white text
- Be clearly visible and clickable
- Have raised borders

**If you DON'T see the rooms:**
- Check the terminal for error messages
- Make sure the server is running: `python advanced_gui/core/network.py`
- Look for messages like: `[CHAT] Requested room list from server`

---

### Step 5: Select a Room

1. **Click on "General" room**

**What you should see:**
- The "General" button turns green/teal (#1abc9c)
- The room title at the top changes to "# General"
- The message area shows any previous messages (if any)

---

### Step 6: Send a Message

1. **In the text box at the bottom, type:**
   ```
   Hello World! This is my first message! 😀
   ```

2. **Click "Send" or press Enter**

**What you should see:**
- Your message appears in the chat area
- Format: `[HH:MM] alice: Hello World! This is my first message! 😀`
- The text box clears

---

### Step 7: Test Emoji Picker

1. **Click the emoji button (😀) on the right side**
2. **An "Emoji Picker" window appears with tabs:**
   - Smileys
   - Emotions
   - Gestures
   - Hearts
   - Symbols
3. **Click any emoji**
4. **The emoji is inserted into your message box**
5. **Type more text and send**

---

### Step 8: Test File Attachment

1. **Click the attachment button (📎)**
2. **A file dialog opens**
3. **Select an image file (.png, .jpg, .jpeg, or .gif)**
4. **The message is sent with format:**
   ```
   [HH:MM] alice: [Image: filename.png]
   ```

---

### Step 9: Switch Rooms

1. **Click on "Projects" room**
2. **The button turns green**
3. **The room title changes to "# Projects"**
4. **The message area clears (no history in this room yet)**
5. **Send a message: "Working on the chat app!"**

---

### Step 10: Test with Multiple Users

**Open a NEW terminal:**
```bash
python advanced_gui/main.py
```

1. **Register as a different user:**
   - Username: `bob`
   - Password: `password123`
2. **Login as bob**
3. **Join the same room (e.g., "General")**
4. **Send a message from bob**
5. **Switch back to alice's window**
6. **You should see bob's message appear!**

---

## 🎯 Expected Layout

```
┌─────────────────────────────────────────────────────────┐
│  Chat App - alice                                       │
├──────────────┬──────────────────────────────────────────┤
│              │  # General                               │
│ Chat Rooms   ├──────────────────────────────────────────┤
│              │                                          │
│  General     │  [10:30] alice: Hello World!            │
│  Projects    │  [10:31] bob: Hi Alice!                 │
│  Friends     │  [10:32] alice: How are you? 😀         │
│              │  [10:33] bob: Great! 👍                  │
│              │                                          │
│              │                                          │
│              ├──────────────────────────────────────────┤
│              │  ┌────────────────────────────────────┐ │
│              │  │ Type your message here...          │ │
│              │  │                                    │ │
│              │  └────────────────────────────────────┘ │
│              │  [😀] [📎] [Send]                       │
└──────────────┴──────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### Problem: Rooms don't appear on the left

**Solution 1:** Check server is running
```bash
# In a terminal, you should see:
[STARTING] Chat server on 127.0.0.1:5556
[LISTENING] Waiting for connections...
```

**Solution 2:** Check for error messages
- Look in the terminal where you ran `python advanced_gui/main.py`
- Look for messages like:
  - `[CHAT] Requested room list from server`
  - `[CHAT] Received 3 rooms from server`
  - `[ROOM PANEL] Updated with 3 rooms`

**Solution 3:** Restart everything
```bash
# Stop the server (Ctrl+C)
# Restart server:
python advanced_gui/core/network.py

# In another terminal:
python advanced_gui/main.py
```

### Problem: Can't register user

**Check:**
- Username must be at least 3 characters
- Password must be at least 6 characters
- Username must be unique (try a different name)

### Problem: Can't login

**Check:**
- Make sure you registered first
- Username and password are case-sensitive
- Try the test user: `testuser` / `testpass123`

### Problem: Messages don't send

**Check:**
- Make sure you selected a room first
- Check that the server is running
- Look for error messages in the terminal

### Problem: GUI doesn't open

**Check:**
- Make sure tkinter is installed: `python -m tkinter`
- On Windows, tkinter comes with Python
- Try reinstalling Python with tkinter support

---

## ✅ Success Checklist

- [ ] Login window appears
- [ ] Can register a new user
- [ ] Can login successfully
- [ ] Chat window opens
- [ ] **3 rooms visible on the left (General, Projects, Friends)**
- [ ] Can click and select a room
- [ ] Selected room turns green
- [ ] Can type and send messages
- [ ] Messages appear in chat area
- [ ] Emoji picker opens and works
- [ ] File attachment dialog opens
- [ ] Can switch between rooms
- [ ] Multiple users can chat together

---

## 🎉 If Everything Works

Congratulations! Your chat application is fully functional!

**Features working:**
✓ User authentication  
✓ Room selection  
✓ Real-time messaging  
✓ Message history  
✓ Emoji support  
✓ File sharing  
✓ Multi-user chat  

**Enjoy your chat app! 💬✨**
