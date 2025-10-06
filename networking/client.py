"""
LAN game client implementation.
Connects to game server and handles communication.
"""

import socket
import threading
import time
from .protocol import (
    MessageType, GameMessage, create_connect_message,
    create_state_update_message, create_game_over_message
)


class GameClient:
    """
    LAN game client for multiplayer Tetris.
    Single responsibility: Connect to server and handle communication.
    """
    
    def __init__(self):
        """Initialize game client."""
        self.socket = None
        self.player_id = None
        self.connected = False
        self.opponent_state = None
        self.lock = threading.Lock()
        self.receive_thread = None
    
    def connect(self, host, port, player_name="Player"):
        """
        Connect to game server.
        
        Args:
            host (str): Server host address
            port (int): Server port
            player_name (str): Player name
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            
            # Send connect message
            msg = create_connect_message(player_name)
            self.socket.sendall(msg.to_bytes())
            
            # Wait for connected response
            response = GameMessage.receive_from_socket(self.socket)
            if response and response.type == MessageType.CONNECTED.value:
                self.player_id = response.player_id
                self.connected = True
                
                # Start receive thread
                self.receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
                self.receive_thread.start()
                
                print(f"Connected to server as {self.player_id}")
                return True
            
            return False
        
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def _receive_messages(self):
        """Receive messages from server in background thread."""
        while self.connected:
            try:
                msg = GameMessage.receive_from_socket(self.socket)
                if not msg:
                    break
                
                self._process_message(msg)
            
            except Exception as e:
                if self.connected:
                    print(f"Error receiving message: {e}")
                break
        
        self.connected = False
        print("Disconnected from server")
    
    def _process_message(self, message):
        """
        Process a message from server.
        
        Args:
            message (GameMessage): Received message
        """
        if message.type == MessageType.STATE_UPDATE.value:
            # Update opponent state
            with self.lock:
                self.opponent_state = message.data.get('state')
        
        elif message.type == MessageType.GAME_OVER.value:
            print(f"Opponent game over. Score: {message.data.get('score', 0)}")
    
    def send_state_update(self, game_state):
        """
        Send game state update to server.
        
        Args:
            game_state (dict): Current game state
        
        Returns:
            bool: True if sent successfully
        """
        if not self.connected:
            return False
        
        try:
            msg = create_state_update_message(self.player_id, game_state)
            self.socket.sendall(msg.to_bytes())
            return True
        except Exception as e:
            print(f"Error sending state update: {e}")
            self.connected = False
            return False
    
    def send_game_over(self, final_score):
        """
        Send game over message to server.
        
        Args:
            final_score (int): Final score
        
        Returns:
            bool: True if sent successfully
        """
        if not self.connected:
            return False
        
        try:
            msg = create_game_over_message(self.player_id, final_score)
            self.socket.sendall(msg.to_bytes())
            return True
        except Exception as e:
            print(f"Error sending game over: {e}")
            return False
    
    def get_opponent_state(self):
        """
        Get the latest opponent state.
        
        Returns:
            dict: Opponent's game state or None
        """
        with self.lock:
            return self.opponent_state
    
    def disconnect(self):
        """Disconnect from server."""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.socket = None
        print("Disconnected")
    
    def is_connected(self):
        """
        Check if currently connected to server.
        
        Returns:
            bool: True if connected
        """
        return self.connected

