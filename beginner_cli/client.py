"""
Beginner CLI Chat Client
A simple TCP client that connects to the chat server.
"""

import socket
import threading
import sys

# Server configuration
HOST = '127.0.0.1'
PORT = 5555


def receive_messages(client_socket):
    """
    Continuously receive and display messages from the server.
    
    Args:
        client_socket: The socket connected to the server
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message, end='')
            else:
                # Server closed the connection
                print("\n[DISCONNECTED] Connection to server lost.")
                break
        except:
            print("\n[ERROR] An error occurred while receiving messages.")
            break


def send_messages(client_socket):
    """
    Read user input and send messages to the server.
    
    Args:
        client_socket: The socket connected to the server
    """
    while True:
        try:
            message = input()
            
            # Check for exit command
            if message.lower() == 'exit':
                print("[EXITING] Closing connection...")
                client_socket.close()
                sys.exit(0)
            
            # Send message to server
            client_socket.send(f"{message}\n".encode('utf-8'))
        
        except KeyboardInterrupt:
            print("\n[EXITING] Closing connection...")
            client_socket.close()
            sys.exit(0)
        except:
            print("[ERROR] Failed to send message.")
            break


def start_client():
    """
    Connect to the chat server and start sending/receiving messages.
    """
    try:
        # Create socket and connect to server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        
        print(f"[CONNECTED] Connected to chat server at {HOST}:{PORT}")
        print("Type your messages and press Enter to send.")
        print("Type 'exit' to quit.\n")
        
        # Start thread to receive messages
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.daemon = True
        receive_thread.start()
        
        # Send messages in main thread
        send_messages(client)
    
    except ConnectionRefusedError:
        print(f"[ERROR] Could not connect to server at {HOST}:{PORT}")
        print("Make sure the server is running.")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")


if __name__ == "__main__":
    start_client()
