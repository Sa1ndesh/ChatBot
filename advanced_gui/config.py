"""
Configuration constants for the advanced chat application.
"""

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5556

# Database configuration
DATABASE_PATH = 'chat_app.db'

# Encryption key (in production, this should be securely managed)
ENCRYPTION_KEY = b'YourSecretEncryptionKey123456789012'  # Must be 32 bytes for Fernet

# UI configuration
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
MESSAGE_HISTORY_LIMIT = 100

# File upload configuration
UPLOAD_FOLDER = 'advanced_gui/assets/uploads'
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}

# Protocol commands
CMD_LOGIN = 'LOGIN'
CMD_REGISTER = 'REGISTER'
CMD_JOIN_ROOM = 'JOIN_ROOM'
CMD_LEAVE_ROOM = 'LEAVE_ROOM'
CMD_SEND_MESSAGE = 'SEND_MESSAGE'
CMD_SEND_FILE = 'SEND_FILE'
CMD_GET_ROOMS = 'GET_ROOMS'
CMD_CREATE_ROOM = 'CREATE_ROOM'
CMD_GET_HISTORY = 'GET_HISTORY'

# Response codes
RESP_SUCCESS = 'SUCCESS'
RESP_ERROR = 'ERROR'
RESP_MESSAGE = 'MESSAGE'
RESP_FILE = 'FILE'
RESP_USER_JOINED = 'USER_JOINED'
RESP_USER_LEFT = 'USER_LEFT'
