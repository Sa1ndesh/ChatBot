"""
Room list panel for displaying and selecting chat rooms.
"""

import tkinter as tk
from tkinter import ttk


class RoomListPanel(tk.Frame):
    """Panel displaying available chat rooms."""
    
    def __init__(self, parent, on_room_select):
        """
        Initialize room list panel.
        
        Args:
            parent: Parent widget
            on_room_select: Callback when room is selected (receives room dict)
        """
        super().__init__(parent, bg="#2c3e50", width=200)
        self.on_room_select = on_room_select
        self.rooms = []
        self.selected_room_id = None
        self.room_buttons = {}
        
        # Prevent the frame from shrinking
        self.pack_propagate(False)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create room list widgets."""
        # Title
        title_label = tk.Label(
            self,
            text="Chat Rooms",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10, padx=10)
        
        # Scrollable frame for rooms
        canvas = tk.Canvas(self, bg="#2c3e50", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.rooms_frame = tk.Frame(canvas, bg="#2c3e50")
        
        self.rooms_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.rooms_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=5)
        scrollbar.pack(side="right", fill="y")
    
    def update_rooms(self, rooms):
        """
        Update the list of rooms.
        
        Args:
            rooms: List of room dictionaries
        """
        print(f"[ROOM PANEL] update_rooms called with {len(rooms)} rooms")
        self.rooms = rooms
        
        # Clear existing buttons
        for widget in self.rooms_frame.winfo_children():
            widget.destroy()
        self.room_buttons.clear()
        
        # Create button for each room
        for room in rooms:
            print(f"[ROOM PANEL] Creating button for room: {room['name']}")
            btn = tk.Button(
                self.rooms_frame,
                text=room['name'],
                font=("Arial", 11, "bold"),
                bg="#34495e",
                fg="white",
                activebackground="#1abc9c",
                activeforeground="white",
                relief=tk.RAISED,
                bd=2,
                cursor="hand2",
                pady=10,
                command=lambda r=room: self.select_room(r)
            )
            btn.pack(fill=tk.X, padx=5, pady=5)
            self.room_buttons[room['id']] = btn
        
        # Force update the display
        self.rooms_frame.update_idletasks()
        self.update_idletasks()
        
        print(f"[ROOM PANEL] Updated with {len(rooms)} rooms, {len(self.room_buttons)} buttons created")
    
    def select_room(self, room):
        """
        Handle room selection.
        
        Args:
            room: Room dictionary
        """
        # Update button colors
        for room_id, btn in self.room_buttons.items():
            if room_id == room['id']:
                btn.config(bg="#1abc9c", relief=tk.SUNKEN)
            else:
                btn.config(bg="#34495e", relief=tk.RAISED)
        
        self.selected_room_id = room['id']
        print(f"[ROOM PANEL] Selected room: {room['name']}")
        self.on_room_select(room)
    
    def highlight_room(self, room_id):
        """
        Highlight a room (for unread messages).
        
        Args:
            room_id: Room ID to highlight
        """
        if room_id in self.room_buttons and room_id != self.selected_room_id:
            self.room_buttons[room_id].config(bg="#e74c3c")
