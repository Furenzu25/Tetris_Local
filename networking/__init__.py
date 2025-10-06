"""
Networking package for LAN multiplayer.
Handles server, client, and protocol for game synchronization.
"""

from .protocol import MessageType, GameMessage
from .server import GameServer
from .client import GameClient

__all__ = ['MessageType', 'GameMessage', 'GameServer', 'GameClient']

