"""
Game board management and collision detection.
Handles the 10x20 Tetris playfield.
"""

from .pieces import Piece, COLORS


class Board:
    """
    Manages the Tetris game board state.
    Single responsibility: Board state and collision detection.
    """
    
    WIDTH = 10
    HEIGHT = 20
    
    def __init__(self):
        """Initialize an empty board."""
        self.grid = [[None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
    
    def is_valid_position(self, piece, x, y):
        """
        Check if a piece can be placed at the given position.
        
        Args:
            piece (Piece): The piece to check
            x (int): X coordinate (column)
            y (int): Y coordinate (row)
        
        Returns:
            bool: True if position is valid, False otherwise
        """
        cells = piece.get_occupied_cells()
        
        for cell_row, cell_col in cells:
            board_row = y + cell_row
            board_col = x + cell_col
            
            # Check boundaries
            if board_col < 0 or board_col >= self.WIDTH:
                return False
            if board_row >= self.HEIGHT:
                return False
            if board_row < 0:
                continue  # Allow pieces above board during spawn
            
            # Check collision with existing blocks
            if self.grid[board_row][board_col] is not None:
                return False
        
        return True
    
    def place_piece(self, piece, x, y):
        """
        Place a piece on the board at the given position.
        
        Args:
            piece (Piece): The piece to place
            x (int): X coordinate (column)
            y (int): Y coordinate (row)
        """
        cells = piece.get_occupied_cells()
        
        for cell_row, cell_col in cells:
            board_row = y + cell_row
            board_col = x + cell_col
            
            if 0 <= board_row < self.HEIGHT and 0 <= board_col < self.WIDTH:
                self.grid[board_row][board_col] = piece.color
    
    def clear_lines(self):
        """
        Clear completed lines and return the number of lines cleared.
        
        Returns:
            int: Number of lines cleared
        """
        lines_to_clear = []
        
        # Find complete lines
        for row in range(self.HEIGHT):
            if all(cell is not None for cell in self.grid[row]):
                lines_to_clear.append(row)
        
        # Remove complete lines
        for row in sorted(lines_to_clear, reverse=True):
            del self.grid[row]
            self.grid.insert(0, [None for _ in range(self.WIDTH)])
        
        return len(lines_to_clear)
    
    def is_game_over(self):
        """
        Check if the game is over (blocks in top rows).
        
        Returns:
            bool: True if game over, False otherwise
        """
        # Check if any blocks in the top 2 rows
        for row in range(2):
            if any(cell is not None for cell in self.grid[row]):
                return True
        return False
    
    def get_drop_position(self, piece, x, y):
        """
        Calculate where a piece would land if hard dropped.
        
        Args:
            piece (Piece): The piece to drop
            x (int): Current X coordinate
            y (int): Current Y coordinate
        
        Returns:
            int: Y coordinate where piece would land
        """
        drop_y = y
        while self.is_valid_position(piece, x, drop_y + 1):
            drop_y += 1
        return drop_y
    
    def get_state(self):
        """
        Get the current board state for serialization.
        
        Returns:
            list[list]: Board grid state
        """
        return [row[:] for row in self.grid]
    
    def set_state(self, state):
        """
        Set the board state from serialized data.
        
        Args:
            state (list[list]): Board grid state
        """
        self.grid = [row[:] for row in state]
    
    def reset(self):
        """Reset the board to empty state."""
        self.grid = [[None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

