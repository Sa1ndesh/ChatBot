"""
Beginner CLI Chat Server
A simple TCP server that broadcasts messages to all connected clients.
"""

import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

# List to keep track of all connected clients
clients = []
clients_lock = threading.Lock()


def broadcast(message, sender_socket=None):
    """
    Send a message to all connected clients except the sender.
    
    Args:
        message: The message to broadcast (bytes)
        sender_socket: The socket of the sender (to exclude from broadcast)
    """
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    # If sending fails, remove the client
                    remove_client(client)


def remove_client(client_socket):
    """
    Remove a client from the clients list.
    
    Args:
        client_socket: The socket to remove
    """
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)


def handle_client(client_socket, address):
    """
    Handle communication with a single client.
    
    Args:
        client_socket: The client's socket
        address: The client's address tuple (ip, port)
    """
    print(f"[NEW CONNECTION] {address} connected.")
    
    # Add client to the list
    with clients_lock:
        clients.append(client_socket)
    
    # Notify all clients about the new connection
    broadcast(f"[SERVER] New user joined the chat!\n".encode('utf-8'), client_socket)
    
    try:
        while True:
            # Receive message from client
            message = client_socket.recv(1024)
            
            if not message:
                # Empty message means client disconnected
                break
            
            # Broadcast the message to all other clients
            print(f"[{address}] {message.decode('utf-8', errors='ignore').strip()}")
            broadcast(f"[{address[0]}:{address[1]}] {message.decode('utf-8', errors='ignore')}".encode('utf-8'), client_socket)
    
    except Exception as e:
        print(f"[ERROR] {address}: {e}")
    
    finally:
        # Clean up when client disconnects
        print(f"[DISCONNECTED] {address} disconnected.")
        remove_client(client_socket)
        broadcast(f"[SERVER] User {address} left the chat.\n".encode('utf-8'))
        client_socket.close()


def start_server():
    """
    Start the chat server and listen for incoming connections.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[STARTING] Server is starting on {HOST}:{PORT}")
        print(f"[LISTENING] Server is listening for connections...")
        
        while True:
            # Accept new connection
            client_socket, address = server.accept()
            
            # Start a new thread to handle this client
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.daemon = True
            thread.start()
            
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    
    except KeyboardInterrupt:
        print("\n[SHUTTING DOWN] Server is shutting down...")
    
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
