"""
Registration window for new users.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.auth import AuthManager
from core.database import Database
from config import DATABASE_PATH


class RegisterWindow(tk.Toplevel):
    """Registration window for creating new accounts."""
    
    def __init__(self, parent):
        """
        Initialize registration window.
        
        Args:
            parent: Parent window
        """
        super().__init__(parent)
        
        self.db = Database(DATABASE_PATH)
        self.auth = AuthManager(self.db)
        
        self.title("Chat App - Register")
        self.geometry("400x350")
        self.resizable(False, False)
        
        self.create_widgets()
        
        # Center window
        self.center_window()
        
        # Make modal
        self.transient(parent)
        self.grab_set()
    
    def center_window(self):
        """Center the window on screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create registration form widgets."""
        # Title
        title_label = tk.Label(
            self,
            text="Create New Account",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)
        
        # Registration frame
        reg_frame = tk.Frame(self)
        reg_frame.pack(pady=20)
        
        # Username
        tk.Label(reg_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=10)
        self.username_entry = tk.Entry(reg_frame, font=("Arial", 12), width=20)
        self.username_entry.grid(row=0, column=1, padx=5, pady=10)
        
        # Email
        tk.Label(reg_frame, text="Email:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        self.email_entry = tk.Entry(reg_frame, font=("Arial", 12), width=20)
        self.email_entry.grid(row=1, column=1, padx=5, pady=10)
        
        # Password
        tk.Label(reg_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5, pady=10)
        self.password_entry = tk.Entry(reg_frame, font=("Arial", 12), width=20, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=10)
        
        # Confirm Password
        tk.Label(reg_frame, text="Confirm:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=5, pady=10)
        self.confirm_entry = tk.Entry(reg_frame, font=("Arial", 12), width=20, show="*")
        self.confirm_entry.grid(row=3, column=1, padx=5, pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        # Register button
        register_btn = tk.Button(
            button_frame,
            text="Register",
            font=("Arial", 12),
            width=10,
            command=self.handle_register
        )
        register_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 12),
            width=10,
            command=self.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        self.confirm_entry.bind('<Return>', lambda e: self.handle_register())
        
        # Focus on username
        self.username_entry.focus()
    
    def handle_register(self):
        """Handle registration button click."""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        
        # Validate input
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Attempt registration
        success, message = self.auth.register_user(username, email, password)
        
        if success:
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.destroy()
        else:
            messagebox.showerror("Registration Failed", message)
