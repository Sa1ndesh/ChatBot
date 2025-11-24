"""
Database operations for the chat application.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple
from .models import User, Room, Message
import os


class Database:
    """Handles all database operations."""
    
    def __init__(self, db_path: str):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with schema."""
        # Read and execute schema
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
        
        with self.get_connection() as conn:
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
            conn.commit()
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, username: str, email: str, password_hash: str) -> Optional[int]:
        """
        Create a new user.
        
        Args:
            username: Unique username
            email: User email
            password_hash: Hashed password
            
        Returns:
            User ID if successful, None otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, password_hash)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username to search for
            
        Returns:
            User object if found, None otherwise
        """
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=datetime.fromisoformat(row['created_at'])
                )
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,)
            ).fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=datetime.fromisoformat(row['created_at'])
                )
            return None
    
    # ==================== ROOM OPERATIONS ====================
    
    def get_all_rooms(self) -> List[Room]:
        """Get all chat rooms."""
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM rooms ORDER BY name").fetchall()
            return [
                Room(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=datetime.fromisoformat(row['created_at'])
                )
                for row in rows
            ]
    
    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        """Get room by ID."""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM rooms WHERE id = ?",
                (room_id,)
            ).fetchone()
            
            if row:
                return Room(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=datetime.fromisoformat(row['created_at'])
                )
            return None
    
    def create_room(self, name: str, description: str = "") -> Optional[int]:
        """Create a new room."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO rooms (name, description) VALUES (?, ?)",
                    (name, description)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    # ==================== MESSAGE OPERATIONS ====================
    
    def save_message(self, room_id: int, sender_id: int, content: str,
                    message_type: str = 'text', file_path: str = None) -> Optional[int]:
        """
        Save a message to the database.
        
        Args:
            room_id: Room ID
            sender_id: Sender user ID
            content: Message content
            message_type: Type of message (text/image)
            file_path: Path to file if applicable
            
        Returns:
            Message ID if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO messages (room_id, sender_id, content, message_type, file_path)
                       VALUES (?, ?, ?, ?, ?)""",
                    (room_id, sender_id, content, message_type, file_path)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"[DB ERROR] Failed to save message: {e}")
            return None
    
    def get_room_messages(self, room_id: int, limit: int = 100) -> List[Message]:
        """
        Get recent messages from a room.
        
        Args:
            room_id: Room ID
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of Message objects
        """
        with self.get_connection() as conn:
            rows = conn.execute(
                """SELECT m.*, u.username as sender_username
                   FROM messages m
                   JOIN users u ON m.sender_id = u.id
                   WHERE m.room_id = ?
                   ORDER BY m.created_at DESC
                   LIMIT ?""",
                (room_id, limit)
            ).fetchall()
            
            messages = [
                Message(
                    id=row['id'],
                    room_id=row['room_id'],
                    sender_id=row['sender_id'],
                    sender_username=row['sender_username'],
                    content=row['content'],
                    message_type=row['message_type'],
                    file_path=row['file_path'],
                    created_at=datetime.fromisoformat(row['created_at'])
                )
                for row in rows
            ]
            
            # Reverse to get chronological order
            return list(reversed(messages))
