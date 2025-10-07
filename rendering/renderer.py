"""
Main renderer for Tetris game using pygame.
Handles all visual elements including board, pieces, UI, and preview.
"""

import pygame
from game_logic.pieces import COLORS
from game_logic.board import Board


class Renderer:
    """
    Handles all rendering for the Tetris game.
    Single responsibility: Visual display and UI rendering.
    """
    
    # Display constants
    CELL_SIZE = 40
    BOARD_WIDTH = Board.WIDTH * CELL_SIZE
    BOARD_HEIGHT = Board.HEIGHT * CELL_SIZE
    PREVIEW_SIZE = 4 * CELL_SIZE
    HOLD_SIZE = 4 * CELL_SIZE
    SIDEBAR_WIDTH = 200
    WINDOW_WIDTH = SIDEBAR_WIDTH + BOARD_WIDTH + SIDEBAR_WIDTH
    WINDOW_HEIGHT = BOARD_HEIGHT + 100
    
    # Colors
    BG_COLOR = (20, 20, 20)
    GRID_COLOR = (50, 50, 50)
    TEXT_COLOR = (255, 255, 255)
    BORDER_COLOR = (100, 100, 100)
    
    def __init__(self):
        """Initialize pygame and create display window."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris LAN Multiplayer")
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Board position (centered)
        self.board_x = self.SIDEBAR_WIDTH
        self.board_y = 50
    
    def render(self, game_engine, opponent_state=None):
        """
        Render the complete game state.
        
        Args:
            game_engine (GameEngine): Current game state
            opponent_state (dict, optional): Opponent's game state for multiplayer
        """
        self.screen.fill(self.BG_COLOR)
        
        # Draw main components
        self._draw_board(game_engine)
        self._draw_current_piece(game_engine)
        self._draw_ghost_piece(game_engine)
        self._draw_hold_piece(game_engine)
        self._draw_next_pieces(game_engine)
        self._draw_stats(game_engine)
        
        # Draw opponent board if in multiplayer
        if opponent_state:
            self._draw_opponent_board(opponent_state)
        
        # Draw game over or pause overlay
        if game_engine.game_over:
            self._draw_game_over()
        elif game_engine.paused:
            self._draw_pause()
        
        pygame.display.flip()
    
    def _draw_board(self, game_engine):
        """Draw the main game board with grid and placed pieces."""
        board = game_engine.board
        
        # Draw border
        border_rect = pygame.Rect(
            self.board_x - 2,
            self.board_y - 2,
            self.BOARD_WIDTH + 4,
            self.BOARD_HEIGHT + 4
        )
        pygame.draw.rect(self.screen, self.BORDER_COLOR, border_rect, 2)
        
        # Draw cells
        for row in range(Board.HEIGHT):
            for col in range(Board.WIDTH):
                x = self.board_x + col * self.CELL_SIZE
                y = self.board_y + row * self.CELL_SIZE
                
                # Draw cell background
                cell_rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
                
                if board.grid[row][col] is not None:
                    # Draw filled cell
                    pygame.draw.rect(self.screen, board.grid[row][col], cell_rect)
                    pygame.draw.rect(self.screen, self.GRID_COLOR, cell_rect, 1)
                else:
                    # Draw grid line
                    pygame.draw.rect(self.screen, self.GRID_COLOR, cell_rect, 1)
    
    def _draw_current_piece(self, game_engine):
        """Draw the currently active piece."""
        if not game_engine.current_piece:
            return
        
        piece = game_engine.current_piece
        cells = piece.get_occupied_cells()
        
        for cell_row, cell_col in cells:
            board_row = game_engine.piece_y + cell_row
            board_col = game_engine.piece_x + cell_col
            
            if 0 <= board_row < Board.HEIGHT and 0 <= board_col < Board.WIDTH:
                x = self.board_x + board_col * self.CELL_SIZE
                y = self.board_y + board_row * self.CELL_SIZE
                
                cell_rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, piece.color, cell_rect)
                pygame.draw.rect(self.screen, self.GRID_COLOR, cell_rect, 1)
    
    def _draw_ghost_piece(self, game_engine):
        """Draw ghost piece showing where current piece will land."""
        if not game_engine.current_piece:
            return
        
        ghost_y = game_engine.get_ghost_position()
        piece = game_engine.current_piece
        cells = piece.get_occupied_cells()
        
        for cell_row, cell_col in cells:
            board_row = ghost_y + cell_row
            board_col = game_engine.piece_x + cell_col
            
            if 0 <= board_row < Board.HEIGHT and 0 <= board_col < Board.WIDTH:
                x = self.board_x + board_col * self.CELL_SIZE
                y = self.board_y + board_row * self.CELL_SIZE
                
                cell_rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, COLORS['GHOST'], cell_rect, 2)
    
    def _draw_hold_piece(self, game_engine):
        """Draw the held piece in the left sidebar."""
        # Draw label
        label = self.font_small.render("HOLD", True, self.TEXT_COLOR)
        self.screen.blit(label, (20, self.board_y))
        
        # Draw hold box
        box_x = 20
        box_y = self.board_y + 30
        box_rect = pygame.Rect(box_x, box_y, self.HOLD_SIZE, self.HOLD_SIZE)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, box_rect, 2)
        
        # Draw piece if exists
        if game_engine.hold_piece:
            self._draw_piece_preview(game_engine.hold_piece, box_x, box_y)
    
    def _draw_next_pieces(self, game_engine):
        """Draw the next 2 pieces in the right sidebar (TETR.IO format)."""
        # Draw label
        label = self.font_small.render("NEXT", True, self.TEXT_COLOR)
        label_x = self.board_x + self.BOARD_WIDTH + 20
        self.screen.blit(label, (label_x, self.board_y))
        
        # Draw next pieces
        for i, piece in enumerate(game_engine.next_pieces[:2]):
            box_x = label_x
            box_y = self.board_y + 30 + i * (self.PREVIEW_SIZE + 10)
            
            # Draw box
            box_rect = pygame.Rect(box_x, box_y, self.PREVIEW_SIZE, self.PREVIEW_SIZE)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, box_rect, 2)
            
            # Draw piece
            self._draw_piece_preview(piece, box_x, box_y)
    
    def _draw_piece_preview(self, piece, x, y):
        """
        Draw a piece in a preview box (centered).
        
        Args:
            piece (Piece): Piece to draw
            x (int): Box X position
            y (int): Box Y position
        """
        cells = piece.get_occupied_cells()
        
        # Calculate piece bounds for centering
        if cells:
            min_row = min(cell[0] for cell in cells)
            max_row = max(cell[0] for cell in cells)
            min_col = min(cell[1] for cell in cells)
            max_col = max(cell[1] for cell in cells)
            
            piece_height = (max_row - min_row + 1) * self.CELL_SIZE
            piece_width = (max_col - min_col + 1) * self.CELL_SIZE
            
            offset_x = (self.PREVIEW_SIZE - piece_width) // 2 - min_col * self.CELL_SIZE
            offset_y = (self.PREVIEW_SIZE - piece_height) // 2 - min_row * self.CELL_SIZE
            
            for cell_row, cell_col in cells:
                cell_x = x + offset_x + cell_col * self.CELL_SIZE
                cell_y = y + offset_y + cell_row * self.CELL_SIZE
                
                cell_rect = pygame.Rect(cell_x, cell_y, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, piece.color, cell_rect)
                pygame.draw.rect(self.screen, self.GRID_COLOR, cell_rect, 1)
    
    def _draw_stats(self, game_engine):
        """Draw score, lines, and level statistics."""
        stats_x = self.board_x + self.BOARD_WIDTH + 20
        stats_y = self.board_y + 300
        
        # Score
        score_label = self.font_small.render("SCORE", True, self.TEXT_COLOR)
        score_value = self.font_medium.render(str(game_engine.score), True, self.TEXT_COLOR)
        self.screen.blit(score_label, (stats_x, stats_y))
        self.screen.blit(score_value, (stats_x, stats_y + 25))
        
        # Lines
        lines_label = self.font_small.render("LINES", True, self.TEXT_COLOR)
        lines_value = self.font_medium.render(str(game_engine.lines_cleared), True, self.TEXT_COLOR)
        self.screen.blit(lines_label, (stats_x, stats_y + 70))
        self.screen.blit(lines_value, (stats_x, stats_y + 95))
        
        # Level
        level_label = self.font_small.render("LEVEL", True, self.TEXT_COLOR)
        level_value = self.font_medium.render(str(game_engine.level), True, self.TEXT_COLOR)
        self.screen.blit(level_label, (stats_x, stats_y + 140))
        self.screen.blit(level_value, (stats_x, stats_y + 165))
    
    def _draw_opponent_board(self, opponent_state):
        """
        Draw opponent's board in miniature.
        
        Args:
            opponent_state (dict): Opponent's game state
        """
        # Draw in bottom right corner
        mini_cell_size = 10
        mini_width = Board.WIDTH * mini_cell_size
        mini_height = Board.HEIGHT * mini_cell_size
        mini_x = self.board_x + self.BOARD_WIDTH + 20
        mini_y = self.WINDOW_HEIGHT - mini_height - 50
        
        # Label
        label = self.font_small.render("OPPONENT", True, self.TEXT_COLOR)
        self.screen.blit(label, (mini_x, mini_y - 25))
        
        # Border
        border_rect = pygame.Rect(mini_x - 1, mini_y - 1, mini_width + 2, mini_height + 2)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, border_rect, 1)
        
        # Draw mini board
        if 'board' in opponent_state:
            board = opponent_state['board']
            for row in range(min(len(board), Board.HEIGHT)):
                for col in range(min(len(board[0]), Board.WIDTH)):
                    if board[row][col] is not None:
                        x = mini_x + col * mini_cell_size
                        y = mini_y + row * mini_cell_size
                        cell_rect = pygame.Rect(x, y, mini_cell_size, mini_cell_size)
                        pygame.draw.rect(self.screen, board[row][col], cell_rect)
    
    def _draw_game_over(self):
        """Draw game over overlay."""
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        restart = self.font_small.render("Press R to restart", True, self.TEXT_COLOR)
        restart_rect = restart.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(restart, restart_rect)
    
    def _draw_pause(self):
        """Draw pause overlay."""
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font_large.render("PAUSED", True, self.TEXT_COLOR)
        text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        self.screen.blit(text, text_rect)
    
    def cleanup(self):
        """Cleanup pygame resources."""
        pygame.quit()

