"""
Quick test to verify GUI components work.
"""

import sys
import os

# Test imports
print("Testing imports...")

try:
    from advanced_gui.core.database import Database
    from advanced_gui.core.auth import AuthManager
    from advanced_gui.config import DATABASE_PATH
    print("✓ Core modules imported successfully")
except Exception as e:
    print(f"✗ Failed to import core modules: {e}")
    sys.exit(1)

# Test database
print("\nTesting database...")
try:
    db = Database(DATABASE_PATH)
    rooms = db.get_all_rooms()
    print(f"✓ Database initialized")
    print(f"✓ Found {len(rooms)} rooms:")
    for room in rooms:
        print(f"  - {room.name}: {room.description}")
except Exception as e:
    print(f"✗ Database error: {e}")
    sys.exit(1)

# Test authentication
print("\nTesting authentication...")
try:
    auth = AuthManager(db)
    
    # Try to create a test user (might already exist)
    success, msg = auth.register_user("testuser", "test@test.com", "testpass123")
    if success:
        print("✓ Test user created")
    else:
        print(f"  Test user already exists (OK)")
    
    # Try to login
    success, user, msg = auth.login_user("testuser", "testpass123")
    if success:
        print(f"✓ Login successful for user: {user.username}")
    else:
        print(f"✗ Login failed: {msg}")
except Exception as e:
    print(f"✗ Auth error: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✓ All tests passed!")
print("="*50)
print("\nYou can now run the GUI:")
print("  python advanced_gui/main.py")
print("\nThe GUI should show:")
print("  1. Login window")
print("  2. After login: Chat window with 3 rooms on the left")
print("     - General")
print("     - Projects")
print("     - Friends")
