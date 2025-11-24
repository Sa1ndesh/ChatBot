"""
Main chat window with room list and message display.
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import socket
import threading
import json
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from core.encryption import MessageEncryption
from ui.room_list_panel import RoomListPanel
from ui.emoji_picker import EmojiPicker


class ChatWindow(tk.Tk):
    """Main chat application window."""
    
    def __init__(self, user):
        """
        Initialize chat window.
        
        Args:
            user: Logged in User object
        """
        super().__init__()
        
        self.user = user
        self.current_room = None
        self.socket = None
        self.encryption = MessageEncryption(ENCRYPTION_KEY)
        
        self.title(f"Chat App - {user.username}")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        self.create_widgets()
        self.connect_to_server()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create chat window widgets."""
        # Main container
        main_container = tk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Room list
        self.room_panel = RoomListPanel(main_container, self.on_room_select)
        self.room_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # Right panel - Chat area
        chat_container = tk.Frame(main_container)
        chat_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Room title
        self.room_title = tk.Label(
            chat_container,
            text="Select a room to start chatting",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            pady=10
        )
        self.room_title.pack(fill=tk.X)
        
        # Message display area
        self.message_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=("Arial", 10),
            state=tk.DISABLED,
            bg="white"
        )
        self.message_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Message input area
        input_frame = tk.Frame(chat_container)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Message entry
        self.message_entry = tk.Text(
            input_frame,
            height=3,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', self.send_message_event)
        self.message_entry.bind('<Shift-Return>', lambda e: None)  # Allow Shift+Enter for newline
        
        # Buttons frame
        buttons_frame = tk.Frame(input_frame)
        buttons_frame.pack(side=tk.RIGHT)
        
        # Emoji button
        emoji_btn = tk.Button(
            buttons_frame,
            text="😀",
            font=("Arial", 12),
            width=3,
            command=self.open_emoji_picker
        )
        emoji_btn.pack(pady=2)
        
        # File button
        file_btn = tk.Button(
            buttons_frame,
            text="📎",
            font=("Arial", 12),
            width=3,
            command=self.attach_file
        )
        file_btn.pack(pady=2)
        
        # Send button
        send_btn = tk.Button(
            buttons_frame,
            text="Send",
            font=("Arial", 10),
            width=6,
            bg="#1abc9c",
            fg="white",
            command=self.send_message
        )
        send_btn.pack(pady=2)
    
    def connect_to_server(self):
        """Connect to the chat server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((SERVER_HOST, SERVER_PORT))
            print(f"[CHAT] Connected to server at {SERVER_HOST}:{SERVER_PORT}")
            
            # Start receiving thread first
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Small delay to ensure receiver is ready
            import time
            time.sleep(0.1)
            
            # Send login message
            login_msg = {
                'action': CMD_LOGIN,
                'username': self.user.username,
                'user_id': self.user.id
            }
            msg_str = json.dumps(login_msg) + '\n'
            print(f"[CHAT] Sending login: {msg_str.strip()}")
            self.socket.send(msg_str.encode('utf-8'))
            
            # Wait a bit for login response
            time.sleep(0.2)
            
            # Get room list
            self.request_rooms()
        
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to server: {e}")
            self.destroy()
    
    def request_rooms(self):
        """Request list of available rooms from server."""
        try:
            msg = {'action': CMD_GET_ROOMS}
            msg_str = json.dumps(msg) + '\n'
            self.socket.send(msg_str.encode('utf-8'))
            print("[CHAT] Requested room list from server")
        except Exception as e:
            print(f"[ERROR] Failed to request rooms: {e}")
    
    def receive_messages(self):
        """Receive messages from server in background thread."""
        buffer = ""
        while True:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    print("[CHAT] Connection closed by server")
                    break
                
                buffer += data
                
                # Process all complete messages (delimited by newlines)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    try:
                        message = json.loads(line)
                        action = message.get('action')
                        print(f"[CHAT] Received action: {action}")
                        
                        if action == RESP_SUCCESS:
                            if 'rooms' in message:
                                print(f"[CHAT] Received {len(message['rooms'])} rooms from server")
                                # Update rooms on main thread
                                self.after(0, lambda: self.room_panel.update_rooms(message['rooms']))
                            elif 'messages' in message:
                                self.after(0, lambda: self.display_history(message['messages']))
                        
                        elif action == RESP_MESSAGE:
                            self.after(0, lambda m=message: self.display_message(m))
                        
                        elif action == RESP_USER_JOINED:
                            username = message['username']
                            self.after(0, lambda u=username: self.display_system_message(f"{u} joined the room"))
                        
                        elif action == RESP_USER_LEFT:
                            username = message['username']
                            self.after(0, lambda u=username: self.display_system_message(f"{u} left the room"))
                        
                        elif action == RESP_ERROR:
                            print(f"[ERROR] {message.get('message')}")
                    
                    except json.JSONDecodeError as e:
                        print(f"[ERROR] Failed to parse JSON: {line[:100]}")
                        print(f"[ERROR] {e}")
            
            except Exception as e:
                print(f"[ERROR] Receive error: {e}")
                import traceback
                traceback.print_exc()
                break
    
    def on_room_select(self, room):
        """
        Handle room selection.
        
        Args:
            room: Room dictionary
        """
        # Leave current room
        if self.current_room:
            leave_msg = {'action': CMD_LEAVE_ROOM}
            try:
                self.socket.send((json.dumps(leave_msg) + '\n').encode('utf-8'))
            except:
                pass
        
        # Join new room
        self.current_room = room
        self.room_title.config(text=f"# {room['name']}")
        
        # Clear message display
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete(1.0, tk.END)
        self.message_display.config(state=tk.DISABLED)
        
        # Join room on server
        join_msg = {
            'action': CMD_JOIN_ROOM,
            'room_id': room['id']
        }
        try:
            self.socket.send((json.dumps(join_msg) + '\n').encode('utf-8'))
            
            # Request message history
            history_msg = {
                'action': CMD_GET_HISTORY,
                'room_id': room['id']
            }
            self.socket.send((json.dumps(history_msg) + '\n').encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] Failed to join room: {e}")
    
    def display_history(self, messages):
        """Display message history."""
        for msg in messages:
            self.display_message(msg, is_history=True)
    
    def display_message(self, message, is_history=False):
        """
        Display a message in the chat window.
        
        Args:
            message: Message dictionary
            is_history: Whether this is a historical message
        """
        username = message.get('username')
        encrypted_content = message.get('content')
        message_type = message.get('message_type', 'text')
        timestamp = message.get('timestamp', datetime.now().isoformat())
        
        # Decrypt content
        content = self.encryption.decrypt(encrypted_content) if encrypted_content else ''
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%H:%M")
        except:
            time_str = "??:??"
        
        # Format message
        if message_type == 'text':
            msg_text = f"[{time_str}] {username}: {content}\n"
        elif message_type == 'image':
            file_path = message.get('file_path', '')
            msg_text = f"[{time_str}] {username}: [Image: {file_path}]\n"
        else:
            msg_text = f"[{time_str}] {username}: [Unknown message]\n"
        
        # Display message
        self.message_display.config(state=tk.NORMAL)
        self.message_display.insert(tk.END, msg_text)
        self.message_display.config(state=tk.DISABLED)
        self.message_display.see(tk.END)
        
        # Highlight room if not current and not history
        if not is_history and self.current_room and message.get('username') != self.user.username:
            # Could add notification here
            pass
    
    def display_system_message(self, text):
        """Display a system message."""
        msg_text = f"[SYSTEM] {text}\n"
        self.message_display.config(state=tk.NORMAL)
        self.message_display.insert(tk.END, msg_text, 'system')
        self.message_display.tag_config('system', foreground='gray')
        self.message_display.config(state=tk.DISABLED)
        self.message_display.see(tk.END)
    
    def send_message_event(self, event):
        """Handle Enter key press."""
        if not event.state & 0x1:  # Check if Shift is not pressed
            self.send_message()
            return 'break'  # Prevent newline
    
    def send_message(self):
        """Send a text message."""
        if not self.current_room:
            messagebox.showwarning("No Room", "Please select a room first")
            return
        
        content = self.message_entry.get(1.0, tk.END).strip()
        if not content:
            return
        
        # Encrypt message
        encrypted_content = self.encryption.encrypt(content)
        
        # Send to server
        msg = {
            'action': CMD_SEND_MESSAGE,
            'content': encrypted_content,
            'message_type': 'text'
        }
        
        try:
            self.socket.send((json.dumps(msg) + '\n').encode('utf-8'))
            self.message_entry.delete(1.0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")
    
    def attach_file(self):
        """Handle file attachment."""
        if not self.current_room:
            messagebox.showwarning("No Room", "Please select a room first")
            return
        
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")]
        )
        
        if file_path:
            # For simplicity, just send filename
            # In production, would upload file to server
            filename = os.path.basename(file_path)
            
            encrypted_content = self.encryption.encrypt(f"Shared image: {filename}")
            
            msg = {
                'action': CMD_SEND_MESSAGE,
                'content': encrypted_content,
                'message_type': 'image',
                'file_path': filename
            }
            
            try:
                self.socket.send((json.dumps(msg) + '\n').encode('utf-8'))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send file: {e}")
    
    def open_emoji_picker(self):
        """Open emoji picker window."""
        EmojiPicker(self, self.insert_emoji)
    
    def insert_emoji(self, emoji):
        """Insert selected emoji into message entry."""
        self.message_entry.insert(tk.INSERT, emoji)
        self.message_entry.focus()
    
    def on_closing(self):
        """Handle window close event."""
        if self.socket:
            try:
                if self.current_room:
                    leave_msg = {'action': CMD_LEAVE_ROOM}
                    self.socket.send((json.dumps(leave_msg) + '\n').encode('utf-8'))
                self.socket.close()
            except:
                pass
        self.destroy()
