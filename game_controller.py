"""
Game controller that handles input and coordinates game components.
Acts as the main coordinator between game logic, rendering, and networking.
"""

import pygame
import time
from game_logic import GameEngine
from rendering import Renderer
from networking import GameClient, GameServer


class GameController:
    """
    Main game controller.
    Single responsibility: Coordinate input, game logic, rendering, and networking.
    """
    
    def __init__(self, mode='single', host=None, port=5555):
        """
        Initialize game controller.
        
        Args:
            mode (str): Game mode ('single', 'host', 'join')
            host (str): Host address for join mode
            port (int): Port number for networking
        """
        self.mode = mode
        self.game_engine = GameEngine()
        self.renderer = Renderer()
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Networking
        self.server = None
        self.client = None
        self.last_state_send = time.time()
        self.state_send_interval = 0.1  # Send state 10 times per second
        
        # Setup networking based on mode
        if mode == 'host':
            self._setup_host(port)
        elif mode == 'join':
            self._setup_client(host, port)
    
    def _setup_host(self, port):
        """Setup as host (server + client)."""
        self.server = GameServer(port=port)
        self.server.start()
        print(f"Hosting game on port {port}")
        print(f"Other players can join with: --mode join --host <your_ip> --port {port}")
        
        # Also connect as client to own server
        self.client = GameClient()
        time.sleep(0.5)  # Give server time to start
        if not self.client.connect('localhost', port):
            print("Warning: Could not connect to own server")
    
    def _setup_client(self, host, port):
        """Setup as client."""
        self.client = GameClient()
        print(f"Connecting to {host}:{port}...")
        if self.client.connect(host, port):
            print("Connected successfully!")
        else:
            print("Connection failed!")
            self.running = False
    
    def handle_input(self, event):
        """
        Handle pygame input events.
        
        Args:
            event (pygame.event.Event): Input event
        """
        if event.type == pygame.QUIT:
            self.running = False
            return
        
        if event.type == pygame.KEYDOWN:
            # Game over restart
            if event.key == pygame.K_r and self.game_engine.game_over:
                self.game_engine.reset()
                return
            
            # Pause
            if event.key == pygame.K_ESCAPE:
                self.game_engine.toggle_pause()
                return
            
            # Don't process game controls if game over or paused
            if self.game_engine.game_over or self.game_engine.paused:
                return
            
            # Movement
            if event.key == pygame.K_LEFT:
                self.game_engine.move_left()
            elif event.key == pygame.K_RIGHT:
                self.game_engine.move_right()
            elif event.key == pygame.K_DOWN:
                self.game_engine.move_down()
            
            # Rotation
            elif event.key == pygame.K_UP or event.key == pygame.K_x:
                self.game_engine.rotate_clockwise()
            elif event.key == pygame.K_z:
                self.game_engine.rotate_counter_clockwise()
            
            # Hard drop
            elif event.key == pygame.K_SPACE:
                self.game_engine.hard_drop()
            
            # Hold
            elif event.key == pygame.K_LSHIFT:
                self.game_engine.hold_current_piece()
    
    def update(self, delta_time):
        """
        Update game state.
        
        Args:
            delta_time (float): Time elapsed since last update
        """
        # Update game engine
        self.game_engine.update(delta_time)
        
        # Send state updates in multiplayer
        if self.client and self.client.is_connected():
            current_time = time.time()
            if current_time - self.last_state_send >= self.state_send_interval:
                state = self.game_engine.get_state()
                self.client.send_state_update(state)
                self.last_state_send = current_time
            
            # Send game over notification
            if self.game_engine.game_over and not hasattr(self, '_game_over_sent'):
                self.client.send_game_over(self.game_engine.score)
                self._game_over_sent = True
    
    def render(self):
        """Render the game."""
        opponent_state = None
        if self.client:
            opponent_state = self.client.get_opponent_state()
        
        self.renderer.render(self.game_engine, opponent_state)
    
    def run(self):
        """Main game loop."""
        if not self.running:
            return
        
        last_time = time.time()
        
        while self.running:
            # Calculate delta time
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time
            
            # Handle events
            for event in pygame.event.get():
                self.handle_input(event)
            
            # Update game
            self.update(delta_time)
            
            # Render
            self.render()
            
            # Cap frame rate
            self.clock.tick(60)
        
        self.cleanup()
    
    def cleanup(self):
        """Cleanup resources."""
        print("Cleaning up...")
        
        # Cleanup networking
        if self.client:
            self.client.disconnect()
        
        if self.server:
            self.server.stop()
        
        # Cleanup renderer
        self.renderer.cleanup()
        
        print("Goodbye!")

