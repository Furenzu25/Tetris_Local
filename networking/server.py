"""
LAN game server implementation.
Manages client connections and game state synchronization.
"""

import socket
import threading
import time
from .protocol import MessageType, GameMessage, create_connected_message, create_state_update_message


class GameServer:
    """
    LAN game server for multiplayer Tetris.
    Single responsibility: Manage client connections and state broadcasting.
    """
    
    def __init__(self, host='0.0.0.0', port=5555):
        """
        Initialize game server.
        
        Args:
            host (str): Host address to bind to
            port (int): Port to listen on
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}  # player_id -> socket
        self.player_states = {}  # player_id -> game_state
        self.running = False
        self.next_player_id = 1
        self.lock = threading.Lock()
    
    def start(self):
        """Start the server and begin accepting connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"Server started on {self.host}:{self.port}")
        
        # Start accept thread
        accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
        accept_thread.start()
    
    def _accept_connections(self):
        """Accept incoming client connections."""
        while self.running:
            try:
                self.server_socket.settimeout(1.0)
                client_socket, address = self.server_socket.accept()
                print(f"New connection from {address}")
                
                # Handle client in new thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")
    
    def _handle_client(self, client_socket, address):
        """
        Handle a connected client.
        
        Args:
            client_socket (socket.socket): Client socket
            address (tuple): Client address
        """
        player_id = None
        
        try:
            # Wait for connect message
            msg = GameMessage.receive_from_socket(client_socket)
            if not msg or msg.type != MessageType.CONNECT.value:
                client_socket.close()
                return
            
            # Assign player ID
            with self.lock:
                player_id = f"player_{self.next_player_id}"
                self.next_player_id += 1
                self.clients[player_id] = client_socket
                self.player_states[player_id] = None
            
            # Send connection confirmation
            response = create_connected_message(player_id)
            client_socket.sendall(response.to_bytes())
            
            print(f"Player {player_id} connected from {address}")
            
            # Handle client messages
            while self.running:
                msg = GameMessage.receive_from_socket(client_socket)
                if not msg:
                    break
                
                self._process_message(player_id, msg)
        
        except Exception as e:
            print(f"Error handling client {player_id}: {e}")
        
        finally:
            # Cleanup
            with self.lock:
                if player_id in self.clients:
                    del self.clients[player_id]
                if player_id in self.player_states:
                    del self.player_states[player_id]
            
            try:
                client_socket.close()
            except:
                pass
            
            print(f"Player {player_id} disconnected")
    
    def _process_message(self, player_id, message):
        """
        Process a message from a client.
        
        Args:
            player_id (str): ID of the player
            message (GameMessage): Received message
        """
        if message.type == MessageType.STATE_UPDATE.value:
            # Update player state and broadcast to others
            with self.lock:
                self.player_states[player_id] = message.data.get('state')
            
            self._broadcast_state_update(player_id)
        
        elif message.type == MessageType.GAME_OVER.value:
            print(f"Player {player_id} game over. Score: {message.data.get('score', 0)}")
            # Could implement game over logic here
    
    def _broadcast_state_update(self, sending_player_id):
        """
        Broadcast player state to other connected clients.
        
        Args:
            sending_player_id (str): ID of player whose state to broadcast
        """
        with self.lock:
            state = self.player_states.get(sending_player_id)
            if not state:
                return
            
            msg = create_state_update_message(sending_player_id, state)
            msg_bytes = msg.to_bytes()
            
            # Send to all other clients
            for player_id, client_socket in list(self.clients.items()):
                if player_id != sending_player_id:
                    try:
                        client_socket.sendall(msg_bytes)
                    except Exception as e:
                        print(f"Error broadcasting to {player_id}: {e}")
    
    def stop(self):
        """Stop the server and close all connections."""
        print("Stopping server...")
        self.running = False
        
        # Close all client connections
        with self.lock:
            for client_socket in self.clients.values():
                try:
                    client_socket.close()
                except:
                    pass
            self.clients.clear()
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("Server stopped")
    
    def get_player_count(self):
        """
        Get number of connected players.
        
        Returns:
            int: Number of connected players
        """
        with self.lock:
            return len(self.clients)

