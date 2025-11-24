"""
Emoji picker window for selecting emojis.
"""

import tkinter as tk
from tkinter import ttk
import json
import os


class EmojiPicker(tk.Toplevel):
    """A simple emoji picker window."""
    
    def __init__(self, parent, callback):
        """
        Initialize emoji picker.
        
        Args:
            parent: Parent window
            callback: Function to call when emoji is selected
        """
        super().__init__(parent)
        self.callback = callback
        self.title("Emoji Picker")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Load emojis
        self.load_emojis()
        
        # Create UI
        self.create_widgets()
        
        # Center window
        self.transient(parent)
        self.grab_set()
    
    def load_emojis(self):
        """Load emojis from JSON file."""
        emoji_file = os.path.join(os.path.dirname(__file__), '..', 'assets', 'emojis.json')
        try:
            with open(emoji_file, 'r', encoding='utf-8') as f:
                self.emojis = json.load(f)
        except:
            # Fallback emojis
            self.emojis = {
                "smileys": ["😀", "😃", "😄", "😁", "😆", "😅"],
                "hearts": ["❤️", "💙", "💚", "💛", "💜", "🖤"],
                "gestures": ["👍", "👎", "👌", "✌️", "👏", "🙌"]
            }
    
    def create_widgets(self):
        """Create emoji picker widgets."""
        # Create notebook for categories
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a tab for each category
        for category, emoji_list in self.emojis.items():
            frame = tk.Frame(notebook)
            notebook.add(frame, text=category.capitalize())
            
            # Create grid of emoji buttons
            row = 0
            col = 0
            for emoji in emoji_list:
                btn = tk.Button(
                    frame,
                    text=emoji,
                    font=("Arial", 20),
                    width=2,
                    height=1,
                    command=lambda e=emoji: self.select_emoji(e)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                
                col += 1
                if col >= 8:
                    col = 0
                    row += 1
    
    def select_emoji(self, emoji):
        """
        Handle emoji selection.
        
        Args:
            emoji: Selected emoji character
        """
        self.callback(emoji)
        self.destroy()
