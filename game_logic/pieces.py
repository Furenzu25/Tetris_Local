"""
Tetromino piece definitions and rotation logic.
Implements SRS (Super Rotation System) rotation states.
"""

# Color definitions (RGB)
COLORS = {
    'I': (0, 255, 255),    # Cyan
    'O': (255, 255, 0),    # Yellow
    'T': (128, 0, 128),    # Purple
    'S': (0, 255, 0),      # Green
    'Z': (255, 0, 0),      # Red
    'J': (0, 0, 255),      # Blue
    'L': (255, 165, 0),    # Orange
    'GHOST': (100, 100, 100),  # Ghost piece
    'EMPTY': (0, 0, 0),    # Empty cell
}

# Tetromino shapes in SRS rotation system (4 rotation states each)
# Format: [rotation_0, rotation_1, rotation_2, rotation_3]
# Each rotation is a 4x4 grid where 1 = filled, 0 = empty
PIECES = {
    'I': [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],
        
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]],
        
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]],
    ],
    'O': [
        [[0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
    ] * 4,  # O piece doesn't rotate
    'T': [
        [[0, 1, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 0, 0],
         [1, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 1, 0, 0],
         [1, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
    ],
    'S': [
        [[0, 1, 1, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 0, 0],
         [0, 1, 1, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0]],
        
        [[1, 0, 0, 0],
         [1, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
    ],
    'Z': [
        [[1, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 1, 0],
         [0, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 0, 0],
         [1, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]],
        
        [[0, 1, 0, 0],
         [1, 1, 0, 0],
         [1, 0, 0, 0],
         [0, 0, 0, 0]],
    ],
    'J': [
        [[1, 0, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 0]],
        
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0]],
    ],
    'L': [
        [[0, 0, 1, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 0, 0],
         [1, 1, 1, 0],
         [1, 0, 0, 0],
         [0, 0, 0, 0]],
        
        [[1, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
    ],
}


class Piece:
    """
    Represents a Tetris piece with type, rotation, and position.
    Single responsibility: Manage piece state and provide shape data.
    """
    
    def __init__(self, piece_type):
        """
        Initialize a new piece.
        
        Args:
            piece_type (str): One of 'I', 'O', 'T', 'S', 'Z', 'J', 'L'
        """
        if piece_type not in PIECES:
            raise ValueError(f"Invalid piece type: {piece_type}")
        
        self.type = piece_type
        self.rotation = 0
        self.color = COLORS[piece_type]
    
    def get_shape(self):
        """
        Get the current shape matrix based on rotation.
        
        Returns:
            list[list[int]]: 4x4 matrix representing piece shape
        """
        return PIECES[self.type][self.rotation]
    
    def rotate_clockwise(self):
        """Rotate the piece 90 degrees clockwise."""
        self.rotation = (self.rotation + 1) % 4
    
    def rotate_counter_clockwise(self):
        """Rotate the piece 90 degrees counter-clockwise."""
        self.rotation = (self.rotation - 1) % 4
    
    def get_occupied_cells(self):
        """
        Get list of (row, col) coordinates occupied by this piece.
        Coordinates are relative to piece's top-left corner.
        
        Returns:
            list[tuple[int, int]]: List of (row, col) coordinates
        """
        shape = self.get_shape()
        cells = []
        for row in range(4):
            for col in range(4):
                if shape[row][col]:
                    cells.append((row, col))
        return cells
    
    def copy(self):
        """
        Create a copy of this piece.
        
        Returns:
            Piece: New piece with same type and rotation
        """
        new_piece = Piece(self.type)
        new_piece.rotation = self.rotation
        return new_piece

