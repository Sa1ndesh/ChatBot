"""
Encryption utilities for secure message transmission.
"""

from cryptography.fernet import Fernet
import base64
import hashlib


class MessageEncryption:
    """Handles encryption and decryption of messages."""
    
    def __init__(self, key: bytes):
        """
        Initialize encryption with a key.
        
        Args:
            key: 32-byte encryption key
        """
        # Ensure key is proper length for Fernet (32 bytes, base64 encoded)
        if len(key) != 32:
            # Hash the key to get exactly 32 bytes
            key = hashlib.sha256(key).digest()
        
        # Fernet requires base64-encoded key
        self.key = base64.urlsafe_b64encode(key)
        self.cipher = Fernet(self.key)
    
    def encrypt(self, message: str) -> str:
        """
        Encrypt a message.
        
        Args:
            message: Plain text message
            
        Returns:
            Encrypted message as base64 string
        """
        try:
            encrypted = self.cipher.encrypt(message.encode('utf-8'))
            return encrypted.decode('utf-8')
        except Exception as e:
            print(f"[ENCRYPTION ERROR] {e}")
            return message
    
    def decrypt(self, encrypted_message: str) -> str:
        """
        Decrypt a message.
        
        Args:
            encrypted_message: Encrypted message as base64 string
            
        Returns:
            Decrypted plain text message
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_message.encode('utf-8'))
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f"[DECRYPTION ERROR] {e}")
            return encrypted_message
