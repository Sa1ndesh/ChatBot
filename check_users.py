"""
Check all users in the database.
"""

from advanced_gui.core.database import Database
from advanced_gui.config import DATABASE_PATH

db = Database(DATABASE_PATH)

print("="*50)
print("Users in Database")
print("="*50)

# Get all users by trying different IDs
for user_id in range(1, 10):
    user = db.get_user_by_id(user_id)
    if user:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

print("="*50)
