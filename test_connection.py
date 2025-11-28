"""
Test connection to server to diagnose issues.
"""

import socket
import json
import time

def test_connection():
    """Test basic connection to server."""
    print("="*50)
    print("Testing Connection to Server")
    print("="*50)
    
    try:
        # Connect to server
        print("\n1. Connecting to server...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 5556))
        print("✓ Connected successfully!")
        
        # Send login message
        print("\n2. Sending login message...")
        login_msg = {
            'action': 'LOGIN',
            'username': 'testuser',
            'user_id': 1
        }
        sock.send((json.dumps(login_msg) + '\n').encode('utf-8'))
        print("✓ Login message sent!")
        
        # Wait for response
        print("\n3. Waiting for response...")
        sock.settimeout(5.0)  # 5 second timeout
        data = sock.recv(4096).decode('utf-8')
        print(f"✓ Received: {data}")
        
        # Parse response
        if '\n' in data:
            line = data.split('\n')[0]
            response = json.loads(line)
            print(f"✓ Parsed response: {response}")
        
        # Request rooms
        print("\n4. Requesting rooms...")
        rooms_msg = {'action': 'GET_ROOMS'}
        sock.send((json.dumps(rooms_msg) + '\n').encode('utf-8'))
        print("✓ Rooms request sent!")
        
        # Wait for rooms response
        print("\n5. Waiting for rooms...")
        data = sock.recv(4096).decode('utf-8')
        print(f"✓ Received: {data[:200]}...")
        
        print("\n" + "="*50)
        print("✓ All tests passed!")
        print("="*50)
        
        sock.close()
        
    except socket.timeout:
        print("\n✗ Timeout - Server not responding")
    except ConnectionRefusedError:
        print("\n✗ Connection refused - Is server running?")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()
