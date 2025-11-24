"""
Login window for user authentication.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.auth import AuthManager
from core.database import Database
from config import DATABASE_PATH


class LoginWindow(tk.Tk):
    """Login window for user authentication."""
    
    def __init__(self, on_login_success):
        """
        Initialize login window.
        
        Args:
            on_login_success: Callback function when login succeeds (receives User object)
        """
        super().__init__()
        
        self.on_login_success = on_login_success
        self.db = Database(DATABASE_PATH)
        self.auth = AuthManager(self.db)
        
        self.title("Chat App - Login")
        self.geometry("400x300")
        self.resizable(False, False)
        
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create login form widgets."""
        # Title
        title_label = tk.Label(
            self,
            text="Welcome to Chat App",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)
        
        # Login frame
        login_frame = tk.Frame(self)
        login_frame.pack(pady=20)
        
        # Username
        tk.Label(login_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=10)
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=20)
        self.username_entry.grid(row=0, column=1, padx=5, pady=10)
        
        # Password
        tk.Label(login_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        # Login button
        login_btn = tk.Button(
            button_frame,
            text="Login",
            font=("Arial", 12),
            width=10,
            command=self.handle_login
        )
        login_btn.pack(side=tk.LEFT, padx=5)
        
        # Register button
        register_btn = tk.Button(
            button_frame,
            text="Register",
            font=("Arial", 12),
            width=10,
            command=self.open_register
        )
        register_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to login
        self.username_entry.bind('<Return>', lambda e: self.handle_login())
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Focus on username
        self.username_entry.focus()
    
    def handle_login(self):
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Attempt login
        success, user, message = self.auth.login_user(username, password)
        
        if success:
            self.withdraw()  # Hide login window
            self.on_login_success(user)
        else:
            messagebox.showerror("Login Failed", message)
            self.password_entry.delete(0, tk.END)
    
    def open_register(self):
        """Open registration window."""
        from ui.register_window import RegisterWindow
        register_window = RegisterWindow(self)
        register_window.wait_window()
