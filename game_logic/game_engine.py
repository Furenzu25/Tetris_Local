"""
Centralized game engine with all Tetris business logic.
Handles game state, scoring, piece management, and game rules.
"""

import random
import time
from .pieces import Piece, PIECES
from .board import Board


class GameEngine:
    """
    Centralized business logic for Tetris game.
    Single responsibility: Manage game rules and state transitions.
    """
    
    # Scoring rules
    SCORE_VALUES = {
        1: 100,   # Single
        2: 300,   # Double
        3: 500,   # Triple
        4: 800,   # Tetris
    }
    
    # Game timing (in seconds)
    LOCK_DELAY = 0.5
    INITIAL_DROP_SPEED = 1.0
    SPEED_INCREASE_PER_LEVEL = 0.1
    
    def __init__(self):
        """Initialize a new game."""
        self.board = Board()
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        
        # Piece management
        self.current_piece = None
        self.piece_x = 0
        self.piece_y = 0
        self.next_pieces = []  # Queue showing next 2 pieces
        self.hold_piece = None
        self.can_hold = True
        
        # Timing
        self.last_drop_time = time.time()
        self.lock_timer = None
        
        # Combo tracking
        self.combo = 0
        
        # Initialize piece queue
        self._fill_piece_queue()
        self._spawn_new_piece()
    
    def _fill_piece_queue(self):
        """Fill the piece queue to show next 2 pieces."""
        piece_types = list(PIECES.keys())
        while len(self.next_pieces) < 2:
            self.next_pieces.append(Piece(random.choice(piece_types)))
    
    def _spawn_new_piece(self):
        """Spawn a new piece at the top of the board."""
        if not self.next_pieces:
            self._fill_piece_queue()
        
        self.current_piece = self.next_pieces.pop(0)
        self._fill_piece_queue()
        
        # Spawn position (centered at top)
        self.piece_x = Board.WIDTH // 2 - 2
        self.piece_y = 0
        
        # Check if spawn position is valid
        if not self.board.is_valid_position(self.current_piece, self.piece_x, self.piece_y):
            self.game_over = True
        
        # Reset hold ability
        self.can_hold = True
        self.lock_timer = None
    
    def move_left(self):
        """
        Move current piece left if possible.
        
        Returns:
            bool: True if move succeeded, False otherwise
        """
        if self.game_over or self.paused or not self.current_piece:
            return False
        
        new_x = self.piece_x - 1
        if self.board.is_valid_position(self.current_piece, new_x, self.piece_y):
            self.piece_x = new_x
            return True
        return False
    
    def move_right(self):
        """
        Move current piece right if possible.
        
        Returns:
            bool: True if move succeeded, False otherwise
        """
        if self.game_over or self.paused or not self.current_piece:
            return False
        
        new_x = self.piece_x + 1
        if self.board.is_valid_position(self.current_piece, new_x, self.piece_y):
            self.piece_x = new_x
            return True
        return False
    
    def move_down(self):
        """
        Move current piece down if possible (soft drop).
        
        Returns:
            bool: True if move succeeded, False if piece locked
        """
        if self.game_over or self.paused or not self.current_piece:
            return False
        
        new_y = self.piece_y + 1
        if self.board.is_valid_position(self.current_piece, self.piece_x, new_y):
            self.piece_y = new_y
            self.lock_timer = None  # Reset lock delay
            return True
        else:
            # Start lock delay if not already started
            if self.lock_timer is None:
                self.lock_timer = time.time()
            return False
    
    def rotate_clockwise(self):
        """
        Rotate current piece clockwise if possible.
        
        Returns:
            bool: True if rotation succeeded, False otherwise
        """
        if self.game_over or self.paused or not self.current_piece:
            return False
        
        self.current_piece.rotate_clockwise()
        if not self.board.is_valid_position(self.current_piece, self.piece_x, self.piece_y):
            # Try wall kicks
            if not self._try_wall_kicks():
                # Rotation failed, revert
                self.current_piece.rotate_counter_clockwise()
                return False
        return True
    
    def rotate_counter_clockwise(self):
        """
        Rotate current piece counter-clockwise if possible.
        
        Returns:
            bool: True if rotation succeeded, False otherwise
        """
        if self.game_over or self.paused or not self.current_piece:
            return False
        
        self.current_piece.rotate_counter_clockwise()
        if not self.board.is_valid_position(self.current_piece, self.piece_x, self.piece_y):
            # Try wall kicks
            if not self._try_wall_kicks():
                # Rotation failed, revert
                self.current_piece.rotate_clockwise()
                return False
        return True
    
    def _try_wall_kicks(self):
        """
        Try wall kick positions for rotation.
        
        Returns:
            bool: True if a valid position was found
        """
        # Simple wall kick: try offsets
        offsets = [(1, 0), (-1, 0), (0, -1), (2, 0), (-2, 0)]
        for dx, dy in offsets:
            if self.board.is_valid_position(self.current_piece, self.piece_x + dx, self.piece_y + dy):
                self.piece_x += dx
                self.piece_y += dy
                return True
        return False
    
    def hard_drop(self):
        """
        Drop piece instantly to the bottom.
        
        Returns:
            int: Number of cells dropped
        """
        if self.game_over or self.paused or not self.current_piece:
            return 0
        
        drop_distance = 0
        while self.board.is_valid_position(self.current_piece, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
            drop_distance += 1
        
        self._lock_piece()
        return drop_distance
    
    def hold_current_piece(self):
        """
        Hold the current piece and swap with held piece.
        
        Returns:
            bool: True if hold succeeded, False otherwise
        """
        if self.game_over or self.paused or not self.can_hold or not self.current_piece:
            return False
        
        if self.hold_piece is None:
            # First hold
            self.hold_piece = Piece(self.current_piece.type)
            self._spawn_new_piece()
        else:
            # Swap pieces
            temp_type = self.hold_piece.type
            self.hold_piece = Piece(self.current_piece.type)
            self.current_piece = Piece(temp_type)
            self.piece_x = Board.WIDTH // 2 - 2
            self.piece_y = 0
        
        self.can_hold = False
        return True
    
    def _lock_piece(self):
        """Lock the current piece to the board and spawn new piece."""
        self.board.place_piece(self.current_piece, self.piece_x, self.piece_y)
        
        # Clear lines and update score
        lines = self.board.clear_lines()
        if lines > 0:
            self._update_score(lines)
            self.combo += 1
        else:
            self.combo = 0
        
        # Check game over
        if self.board.is_game_over():
            self.game_over = True
        else:
            self._spawn_new_piece()
    
    def _update_score(self, lines_cleared):
        """
        Update score based on lines cleared.
        
        Args:
            lines_cleared (int): Number of lines cleared
        """
        base_score = self.SCORE_VALUES.get(lines_cleared, 0)
        combo_bonus = self.combo * 50
        level_multiplier = self.level
        
        self.score += (base_score + combo_bonus) * level_multiplier
        self.lines_cleared += lines_cleared
        
        # Level up every 10 lines
        new_level = (self.lines_cleared // 10) + 1
        if new_level > self.level:
            self.level = new_level
    
    def update(self, delta_time):
        """
        Update game state based on elapsed time.
        
        Args:
            delta_time (float): Time elapsed since last update
        """
        if self.game_over or self.paused:
            return
        
        current_time = time.time()
        
        # Check lock delay
        if self.lock_timer is not None:
            if current_time - self.lock_timer >= self.LOCK_DELAY:
                self._lock_piece()
                return
        
        # Auto drop
        drop_speed = max(0.1, self.INITIAL_DROP_SPEED - (self.level - 1) * self.SPEED_INCREASE_PER_LEVEL)
        if current_time - self.last_drop_time >= drop_speed:
            self.move_down()
            self.last_drop_time = current_time
    
    def get_ghost_position(self):
        """
        Get the Y position where current piece would land.
        
        Returns:
            int: Y coordinate of ghost piece
        """
        if not self.current_piece:
            return 0
        return self.board.get_drop_position(self.current_piece, self.piece_x, self.piece_y)
    
    def toggle_pause(self):
        """Toggle pause state."""
        if not self.game_over:
            self.paused = not self.paused
    
    def reset(self):
        """Reset the game to initial state."""
        self.__init__()
    
    def get_state(self):
        """
        Get complete game state for serialization.
        
        Returns:
            dict: Complete game state
        """
        return {
            'board': self.board.get_state(),
            'score': self.score,
            'lines_cleared': self.lines_cleared,
            'level': self.level,
            'game_over': self.game_over,
            'current_piece': {
                'type': self.current_piece.type if self.current_piece else None,
                'rotation': self.current_piece.rotation if self.current_piece else 0,
                'x': self.piece_x,
                'y': self.piece_y,
            },
            'next_pieces': [p.type for p in self.next_pieces],
            'hold_piece': self.hold_piece.type if self.hold_piece else None,
        }

