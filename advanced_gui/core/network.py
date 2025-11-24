"""
Network server for the advanced chat application.
Handles multiple clients and chat rooms.
"""

import socket
import threading
import json
import os
from typing import Dict, List
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from core.database import Database
from core.auth import AuthManager
from core.encryption import MessageEncryption


class ChatServer:
    """Multi-room chat server."""
    
    def __init__(self):
        """Initialize the chat server."""
        self.host = SERVER_HOST
        self.port = SERVER_PORT
        self.db = Database(DATABASE_PATH)
        self.auth = AuthManager(self.db)
        self.encryption = MessageEncryption(ENCRYPTION_KEY)
        
        # Track connected clients: {socket: {'user_id': int, 'username': str, 'room_id': int}}
        self.clients: Dict[socket.socket, dict] = {}
        self.clients_lock = threading.Lock()
        
        # Track clients by room: {room_id: [socket1, socket2, ...]}
        self.rooms: Dict[int, List[socket.socket]] = {}
        
        # Ensure upload folder exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    def broadcast_to_room(self, room_id: int, message: dict, exclude_socket=None):
        """
        Broadcast a message to all clients in a room.
        
        Args:
            room_id: Room ID to broadcast to
            message: Message dictionary
            exclude_socket: Socket to exclude from broadcast
        """
        if room_id not in self.rooms:
            return
        
        message_json = json.dumps(message)
        
        with self.clients_lock:
            for client_socket in self.rooms[room_id][:]:  # Copy list to avoid modification during iteration
                if client_socket != exclude_socket:
                    try:
                        # Add newline delimiter
                        client_socket.send((message_json + '\n').encode('utf-8'))
                    except Exception as e:
                        print(f"[SERVER] Error broadcasting: {e}")
                        self.remove_client(client_socket)
    
    def send_to_client(self, client_socket: socket.socket, message: dict):
        """Send a message to a specific client."""
        try:
            message_json = json.dumps(message)
            # Add newline delimiter to help with message parsing
            client_socket.send((message_json + '\n').encode('utf-8'))
        except Exception as e:
            print(f"[SERVER] Error sending to client: {e}")
            self.remove_client(client_socket)
    
    def remove_client(self, client_socket: socket.socket):
        """Remove a client from all tracking structures."""
        with self.clients_lock:
            if client_socket in self.clients:
                client_info = self.clients[client_socket]
                room_id = client_info.get('room_id')
                username = client_info.get('username', 'Unknown')
                
                # Remove from room
                if room_id and room_id in self.rooms:
                    if client_socket in self.rooms[room_id]:
                        self.rooms[room_id].remove(client_socket)
                    
                    # Notify others in room
                    self.broadcast_to_room(room_id, {
                        'action': RESP_USER_LEFT,
                        'username': username
                    })
                
                # Remove from clients
                del self.clients[client_socket]
            
            try:
                client_socket.close()
            except:
                pass
    
    def handle_client(self, client_socket: socket.socket, address):
        """Handle communication with a client."""
        print(f"[NEW CONNECTION] {address} connected")
        
        buffer = ""
        try:
            while True:
                # Receive data
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                
                # Process all complete messages (delimited by newlines)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    # Parse JSON message
                    try:
                        message = json.loads(line)
                        action = message.get('action')
                        print(f"[SERVER] Received action: {action} from {address}")
                        
                        if action == CMD_LOGIN:
                            self.handle_login(client_socket, message)
                        elif action == CMD_JOIN_ROOM:
                            self.handle_join_room(client_socket, message)
                        elif action == CMD_LEAVE_ROOM:
                            self.handle_leave_room(client_socket, message)
                        elif action == CMD_SEND_MESSAGE:
                            self.handle_send_message(client_socket, message)
                        elif action == CMD_GET_ROOMS:
                            self.handle_get_rooms(client_socket)
                        elif action == CMD_GET_HISTORY:
                            self.handle_get_history(client_socket, message)
                        else:
                            self.send_to_client(client_socket, {
                                'action': RESP_ERROR,
                                'message': 'Unknown action'
                            })
                    
                    except json.JSONDecodeError as e:
                        print(f"[ERROR] Invalid JSON from {address}: {line[:100]}")
                        print(f"[ERROR] {e}")
        
        except Exception as e:
            print(f"[ERROR] {address}: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.remove_client(client_socket)
            print(f"[DISCONNECTED] {address}")
    
    def handle_login(self, client_socket: socket.socket, message: dict):
        """Handle user login."""
        username = message.get('username')
        user_id = message.get('user_id')
        
        user = self.db.get_user_by_id(user_id)
        if user and user.username == username:
            with self.clients_lock:
                self.clients[client_socket] = {
                    'user_id': user_id,
                    'username': username,
                    'room_id': None
                }
            
            self.send_to_client(client_socket, {
                'action': RESP_SUCCESS,
                'message': 'Login successful'
            })
        else:
            self.send_to_client(client_socket, {
                'action': RESP_ERROR,
                'message': 'Invalid credentials'
            })
    
    def handle_join_room(self, client_socket: socket.socket, message: dict):
        """Handle client joining a room."""
        room_id = message.get('room_id')
        
        if client_socket not in self.clients:
            return
        
        with self.clients_lock:
            # Leave current room if any
            current_room = self.clients[client_socket].get('room_id')
            if current_room and current_room in self.rooms:
                if client_socket in self.rooms[current_room]:
                    self.rooms[current_room].remove(client_socket)
            
            # Join new room
            self.clients[client_socket]['room_id'] = room_id
            if room_id not in self.rooms:
                self.rooms[room_id] = []
            self.rooms[room_id].append(client_socket)
        
        username = self.clients[client_socket]['username']
        
        # Notify others in room
        self.broadcast_to_room(room_id, {
            'action': RESP_USER_JOINED,
            'username': username
        }, exclude_socket=client_socket)
        
        # Confirm to client
        self.send_to_client(client_socket, {
            'action': RESP_SUCCESS,
            'message': f'Joined room {room_id}'
        })
    
    def handle_leave_room(self, client_socket: socket.socket, message: dict):
        """Handle client leaving a room."""
        if client_socket not in self.clients:
            return
        
        with self.clients_lock:
            room_id = self.clients[client_socket].get('room_id')
            username = self.clients[client_socket].get('username')
            
            if room_id and room_id in self.rooms:
                if client_socket in self.rooms[room_id]:
                    self.rooms[room_id].remove(client_socket)
                
                # Notify others
                self.broadcast_to_room(room_id, {
                    'action': RESP_USER_LEFT,
                    'username': username
                })
            
            self.clients[client_socket]['room_id'] = None
    
    def handle_send_message(self, client_socket: socket.socket, message: dict):
        """Handle sending a message."""
        if client_socket not in self.clients:
            return
        
        client_info = self.clients[client_socket]
        room_id = client_info.get('room_id')
        user_id = client_info.get('user_id')
        username = client_info.get('username')
        
        if not room_id:
            self.send_to_client(client_socket, {
                'action': RESP_ERROR,
                'message': 'Not in a room'
            })
            return
        
        # Decrypt message content
        encrypted_content = message.get('content')
        content = self.encryption.decrypt(encrypted_content)
        message_type = message.get('message_type', 'text')
        file_path = message.get('file_path')
        
        # Save to database
        msg_id = self.db.save_message(room_id, user_id, content, message_type, file_path)
        
        if msg_id:
            # Broadcast to room (re-encrypt for transmission)
            self.broadcast_to_room(room_id, {
                'action': RESP_MESSAGE,
                'username': username,
                'content': encrypted_content,  # Send encrypted
                'message_type': message_type,
                'file_path': file_path,
                'timestamp': datetime.now().isoformat()
            })
    
    def handle_get_rooms(self, client_socket: socket.socket):
        """Send list of available rooms to client."""
        rooms = self.db.get_all_rooms()
        self.send_to_client(client_socket, {
            'action': RESP_SUCCESS,
            'rooms': [{'id': r.id, 'name': r.name, 'description': r.description} for r in rooms]
        })
    
    def handle_get_history(self, client_socket: socket.socket, message: dict):
        """Send message history for a room."""
        room_id = message.get('room_id')
        messages = self.db.get_room_messages(room_id, MESSAGE_HISTORY_LIMIT)
        
        # Encrypt messages for transmission
        encrypted_messages = []
        for msg in messages:
            encrypted_messages.append({
                'username': msg.sender_username,
                'content': self.encryption.encrypt(msg.content) if msg.content else '',
                'message_type': msg.message_type,
                'file_path': msg.file_path,
                'timestamp': msg.created_at.isoformat()
            })
        
        self.send_to_client(client_socket, {
            'action': RESP_SUCCESS,
            'messages': encrypted_messages
        })
    
    def start(self):
        """Start the chat server."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server.bind((self.host, self.port))
            server.listen()
            print(f"[STARTING] Chat server on {self.host}:{self.port}")
            print(f"[LISTENING] Waiting for connections...")
            
            while True:
                client_socket, address = server.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                thread.daemon = True
                thread.start()
        
        except KeyboardInterrupt:
            print("\n[SHUTTING DOWN] Server stopping...")
        finally:
            server.close()


if __name__ == "__main__":
    server = ChatServer()
    server.start()
