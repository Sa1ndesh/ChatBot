"""
Main entry point for the advanced GUI chat application.
"""

from ui.login_window import LoginWindow
from ui.chat_window import ChatWindow


def on_login_success(user):
    """
    Callback when user successfully logs in.
    
    Args:
        user: Authenticated User object
    """
    # Create and show chat window
    chat_window = ChatWindow(user)
    chat_window.mainloop()


def main():
    """Start the application."""
    # Show login window
    login_window = LoginWindow(on_login_success)
    login_window.mainloop()


if __name__ == "__main__":
    main()
