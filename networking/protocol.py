"""
Network protocol definitions for LAN multiplayer.
Defines message types and serialization.
"""

import json
import time
from enum import Enum


class MessageType(Enum):
    """Enum for different message types."""
    CONNECT = "connect"
    CONNECTED = "connected"
    INPUT = "input"
    STATE_UPDATE = "state_update"
    LINE_CLEAR = "line_clear"
    GAME_OVER = "game_over"
    DISCONNECT = "disconnect"
    PING = "ping"
    PONG = "pong"


class GameMessage:
    """
    Represents a network message.
    Single responsibility: Message creation and serialization.
    """
    
    def __init__(self, message_type, player_id=None, data=None):
        """
        Create a new game message.
        
        Args:
            message_type (MessageType): Type of message
            player_id (str, optional): ID of the player sending message
            data (dict, optional): Message payload
        """
        self.type = message_type
        self.player_id = player_id
        self.data = data or {}
        self.timestamp = time.time()
    
    def to_json(self):
        """
        Serialize message to JSON string.
        
        Returns:
            str: JSON representation of message
        """
        return json.dumps({
            'type': self.type.value if isinstance(self.type, MessageType) else self.type,
            'player_id': self.player_id,
            'data': self.data,
            'timestamp': self.timestamp,
        })
    
    @staticmethod
    def from_json(json_str):
        """
        Deserialize message from JSON string.
        
        Args:
            json_str (str): JSON string
        
        Returns:
            GameMessage: Deserialized message
        """
        try:
            obj = json.loads(json_str)
            msg = GameMessage(
                message_type=obj['type'],
                player_id=obj.get('player_id'),
                data=obj.get('data', {})
            )
            msg.timestamp = obj.get('timestamp', time.time())
            return msg
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error deserializing message: {e}")
            return None
    
    def to_bytes(self):
        """
        Convert message to bytes for transmission.
        
        Returns:
            bytes: Message as bytes with length prefix
        """
        json_str = self.to_json()
        json_bytes = json_str.encode('utf-8')
        length = len(json_bytes)
        # 4-byte length prefix + message
        return length.to_bytes(4, byteorder='big') + json_bytes
    
    @staticmethod
    def receive_from_socket(sock):
        """
        Receive a complete message from socket.
        
        Args:
            sock (socket.socket): Socket to receive from
        
        Returns:
            GameMessage: Received message or None if failed
        """
        try:
            # Read 4-byte length prefix
            length_bytes = sock.recv(4)
            if not length_bytes or len(length_bytes) < 4:
                return None
            
            length = int.from_bytes(length_bytes, byteorder='big')
            
            # Read the message
            message_bytes = b''
            while len(message_bytes) < length:
                chunk = sock.recv(min(length - len(message_bytes), 4096))
                if not chunk:
                    return None
                message_bytes += chunk
            
            json_str = message_bytes.decode('utf-8')
            return GameMessage.from_json(json_str)
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None


def create_connect_message(player_name):
    """Create a connection request message."""
    return GameMessage(MessageType.CONNECT, data={'player_name': player_name})


def create_connected_message(player_id):
    """Create a connection acknowledgment message."""
    return GameMessage(MessageType.CONNECTED, player_id=player_id)


def create_input_message(player_id, action, params=None):
    """Create an input action message."""
    return GameMessage(
        MessageType.INPUT,
        player_id=player_id,
        data={'action': action, 'params': params or {}}
    )


def create_state_update_message(player_id, game_state):
    """Create a game state update message."""
    return GameMessage(
        MessageType.STATE_UPDATE,
        player_id=player_id,
        data={'state': game_state}
    )


def create_game_over_message(player_id, final_score):
    """Create a game over message."""
    return GameMessage(
        MessageType.GAME_OVER,
        player_id=player_id,
        data={'score': final_score}
    )

