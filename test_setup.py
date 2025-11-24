"""
Test script to verify the chat application setup.
"""

import os
import sys

def check_file_exists(filepath):
    """Check if a file exists."""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {filepath}")
    return exists

def main():
    print("=" * 60)
    print("Chat Application Setup Verification")
    print("=" * 60)
    
    print("\n1. Checking Beginner CLI Files:")
    cli_files = [
        "beginner_cli/server.py",
        "beginner_cli/client.py",
        "beginner_cli/__init__.py"
    ]
    cli_ok = all(check_file_exists(f) for f in cli_files)
    
    print("\n2. Checking Advanced GUI Core Files:")
    core_files = [
        "advanced_gui/config.py",
        "advanced_gui/schema.sql",
        "advanced_gui/main.py",
        "advanced_gui/core/database.py",
        "advanced_gui/core/auth.py",
        "advanced_gui/core/encryption.py",
        "advanced_gui/core/models.py",
        "advanced_gui/core/network.py"
    ]
    core_ok = all(check_file_exists(f) for f in core_files)
    
    print("\n3. Checking Advanced GUI UI Files:")
    ui_files = [
        "advanced_gui/ui/login_window.py",
        "advanced_gui/ui/register_window.py",
        "advanced_gui/ui/chat_window.py",
        "advanced_gui/ui/room_list_panel.py",
        "advanced_gui/ui/emoji_picker.py"
    ]
    ui_ok = all(check_file_exists(f) for f in ui_files)
    
    print("\n4. Checking Assets:")
    asset_files = [
        "advanced_gui/assets/emojis.json"
    ]
    assets_ok = all(check_file_exists(f) for f in asset_files)
    
    print("\n5. Checking Documentation:")
    doc_files = [
        "README.md",
        "QUICKSTART.md",
        "requirements.txt"
    ]
    docs_ok = all(check_file_exists(f) for f in doc_files)
    
    print("\n6. Checking Dependencies:")
    try:
        import bcrypt
        print("✓ bcrypt installed")
        bcrypt_ok = True
    except ImportError:
        print("✗ bcrypt NOT installed - run: pip install bcrypt")
        bcrypt_ok = False
    
    try:
        import cryptography
        print("✓ cryptography installed")
        crypto_ok = True
    except ImportError:
        print("✗ cryptography NOT installed - run: pip install cryptography")
        crypto_ok = False
    
    try:
        import tkinter
        print("✓ tkinter available")
        tk_ok = True
    except ImportError:
        print("✗ tkinter NOT available - install python3-tk")
        tk_ok = False
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    all_ok = cli_ok and core_ok and ui_ok and assets_ok and docs_ok and bcrypt_ok and crypto_ok and tk_ok
    
    if all_ok:
        print("✓ All checks passed! Your chat application is ready to run.")
        print("\nTo get started:")
        print("1. Start CLI server: python beginner_cli/server.py")
        print("2. Start CLI client: python beginner_cli/client.py")
        print("\nOR")
        print("\n1. Start GUI server: python advanced_gui/core/network.py")
        print("2. Start GUI client: python advanced_gui/main.py")
    else:
        print("✗ Some checks failed. Please review the errors above.")
        if not (bcrypt_ok and crypto_ok):
            print("\nInstall missing dependencies:")
            print("  pip install -r requirements.txt")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
