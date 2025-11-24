"""
Authentication logic for user registration and login.
"""

import bcrypt
from typing import Optional, Tuple
from .database import Database
from .models import User


class AuthManager:
    """Handles user authentication."""
    
    def __init__(self, database: Database):
        """
        Initialize authentication manager.
        
        Args:
            database: Database instance
        """
        self.db = database
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password as string
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            password_hash: Stored password hash
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except:
            return False
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            username: Desired username
            email: User email
            password: Plain text password
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate input
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        # Check if username already exists
        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            return False, "Username already exists"
        
        # Hash password and create user
        password_hash = self.hash_password(password)
        user_id = self.db.create_user(username, email, password_hash)
        
        if user_id:
            return True, "Registration successful"
        else:
            return False, "Failed to create user"
    
    def login_user(self, username: str, password: str) -> Tuple[bool, Optional[User], str]:
        """
        Authenticate a user.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            Tuple of (success: bool, user: Optional[User], message: str)
        """
        # Get user from database
        user = self.db.get_user_by_username(username)
        
        if not user:
            return False, None, "Invalid username or password"
        
        # Verify password
        if self.verify_password(password, user.password_hash):
            return True, user, "Login successful"
        else:
            return False, None, "Invalid username or password"
