"""
Test to verify rooms display correctly in the GUI.
"""

import tkinter as tk
from advanced_gui.ui.room_list_panel import RoomListPanel

def test_room_panel():
    """Test the room panel displays rooms correctly."""
    
    # Create test window
    root = tk.Tk()
    root.title("Room Panel Test")
    root.geometry("300x400")
    
    # Create room panel
    def on_room_select(room):
        print(f"Selected room: {room['name']}")
    
    panel = RoomListPanel(root, on_room_select)
    panel.pack(fill=tk.BOTH, expand=True)
    
    # Test data - same format as server sends
    test_rooms = [
        {'id': 1, 'name': 'General', 'description': 'General discussion room'},
        {'id': 2, 'name': 'Projects', 'description': 'Project-related discussions'},
        {'id': 3, 'name': 'Friends', 'description': 'Casual chat with friends'}
    ]
    
    # Update rooms after a short delay
    def update_test_rooms():
        print("Updating rooms...")
        panel.update_rooms(test_rooms)
        print("Rooms updated!")
    
    root.after(500, update_test_rooms)
    
    print("="*50)
    print("Room Panel Test")
    print("="*50)
    print("You should see:")
    print("1. 'Chat Rooms' title at the top")
    print("2. Three room buttons:")
    print("   - General")
    print("   - Projects")
    print("   - Friends")
    print("3. Buttons should be dark gray with white text")
    print("4. Click a button to select it (turns green)")
    print("="*50)
    
    root.mainloop()

if __name__ == "__main__":
    test_room_panel()
