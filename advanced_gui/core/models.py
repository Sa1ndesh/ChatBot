"""
Data models for the chat application.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Represents a user in the chat system."""
    id: int
    username: str
    email: Optional[str]
    password_hash: str
    created_at: datetime


@dataclass
class Room:
    """Represents a chat room."""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime


@dataclass
class Message:
    """Represents a chat message."""
    id: int
    room_id: int
    sender_id: int
    sender_username: str
    content: Optional[str]
    message_type: str
    file_path: Optional[str]
    created_at: datetime
    
    def __str__(self):
        """Format message for display."""
        timestamp = self.created_at.strftime("%H:%M")
        if self.message_type == 'text':
            return f"[{timestamp}] {self.sender_username}: {self.content}"
        elif self.message_type == 'image':
            return f"[{timestamp}] {self.sender_username}: [Image: {self.file_path}]"
        return f"[{timestamp}] {self.sender_username}: [Unknown message type]"
