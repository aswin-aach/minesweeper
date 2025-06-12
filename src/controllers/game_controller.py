import time
import traceback
from datetime import datetime
from src.models.board import Board
from src.models.high_score import HighScoreManager
import os

class GameController:
    """
    Controller for the Minesweeper game.
    
    Manages game state, timer, flag counting, and high scores.
    
    Attributes:
        board (Board): The game board.
        game_state (str): Current state of the game ('new', 'in_progress', 'won', 'lost').
        start_time (float): Time when the game started (in seconds since epoch).
        elapsed_time (int): Time elapsed since the game started (in seconds).
        total_mines (int): Total number of mines on the board.
        flags_placed (int): Number of flags placed by the player.
        high_score_manager (HighScoreManager): Manager for high scores.
    """
    
    def __init__(self, rows=16, cols=16, mines=40):
        """
        Initialize a new game controller.
        
        Args:
            rows (int, optional): Number of rows in the board. Defaults to 16.
            cols (int, optional): Number of columns in the board. Defaults to 16.
            mines (int, optional): Number of mines to place. Defaults to 40.
        """
        self.board = Board(rows, cols, mines)
        self.game_state = 'new'
        self.start_time = 0
        self.elapsed_time = 0
        self.total_mines = mines
        self.flags_placed = 0
        self.high_score_manager = HighScoreManager()
    
    def start_game(self):
        """Start a new game by placing mines and starting the timer."""
        if self.game_state == 'new':
            self.board.place_mines(self.total_mines)
            self.start_time = time.time()
            self.game_state = 'in_progress'
            
    def debug_reveal_all(self):
        """Debug function to reveal all non-mine cells."""
        if self.game_state == 'new':
            self.start_game()
        elif self.game_state != 'in_progress':
            return None
            
        revealed_cells = []
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                cell = self.board.grid[row][col]
                if not cell.is_mine and not cell.is_revealed:
                    cell.is_revealed = True
                    revealed_cells.append({
                        'row': row,
                        'col': col,
                        'adjacent_mines': cell.adjacent_mines
                    })
        
        # Update elapsed time before checking win
        if self.start_time > 0:
            self.elapsed_time = time.time() - self.start_time
        
        # Check if all non-mine cells are revealed
        if self.board.check_win():
            self.handle_win()
        
        return {
            'revealed_cells': revealed_cells,
            'game_state': self.game_state,
            'mines_remaining': self.get_remaining_mines(),
            'elapsed_time': self.get_elapsed_time(),
            'won': self.game_state == 'won'
        }
    
    def restart_game(self):
        """Restart the game by resetting the board and game state."""
        self.board = Board(self.board.rows, self.board.cols, self.total_mines)
        self.game_state = 'new'
        self.start_time = 0
        self.elapsed_time = 0
        self.flags_placed = 0
        self.start_game()
    
    def get_elapsed_time(self):
        """
        Get the elapsed time since the game started.
        
        Returns:
            int: Elapsed time in seconds.
        """
        if self.game_state == 'new':
            return 0
        elif self.game_state in ['won', 'lost']:
            return self.elapsed_time
        else:  # in_progress
            current_time = time.time()
            return int(current_time - self.start_time)
    
    def get_remaining_mines(self):
        """
        Get the number of remaining unflagged mines.
        
        Returns:
            int: Number of mines minus number of flags placed.
        """
        return self.total_mines - self.flags_placed
    
    def chord_reveal(self, row, col):
        """
        Reveal all adjacent cells when middle-clicking a revealed number if the correct
        number of flags are placed around it.
        
        Args:
            row (int): The row index
            col (int): The column index
            
        Returns:
            dict: Information about the revealed cells and game state
        """
        if self.game_state != 'in_progress':
            return None
            
        cell = self.board.get_cell(row, col)
        if not cell or not cell.is_revealed or cell.adjacent_mines == 0:
            return None
            
        # Count flagged neighbors
        flagged_count = 0
        neighbors = []
        
        # Check all 8 adjacent cells
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                    
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                    neighbor = self.board.get_cell(new_row, new_col)
                    if neighbor.is_flagged:
                        flagged_count += 1
                    elif not neighbor.is_revealed:
                        neighbors.append((new_row, new_col))
        
        # If flagged neighbors match the number, reveal all unflagged neighbors
        if flagged_count == cell.adjacent_mines:
            revealed_cells = []
            game_over = False
            won = False
            
            for n_row, n_col in neighbors:
                neighbor = self.board.get_cell(n_row, n_col)
                if neighbor.is_mine:
                    # Game over if we reveal a mine
                    self.game_state = 'lost'
                    game_over = True
                    break
                else:
                    # Reveal the cell
                    if self.board.reveal_cell(n_row, n_col):
                        cell = self.board.get_cell(n_row, n_col)
                        revealed_cells.append({
                            'row': n_row,
                            'col': n_col,
                            'adjacent_mines': cell.adjacent_mines,
                            'is_mine': cell.is_mine
                        })
            
            # Check if we've won
            if not game_over and self.board._check_win_condition():
                self.game_state = 'won'
                game_over = True
                won = True
                self.handle_win()
            
            return {
                'revealed_cells': revealed_cells,
                'game_state': self.game_state,
                'game_over': game_over,
                'won': won,
                'mines_remaining': self.get_remaining_mines(),
                'elapsed_time': self.get_elapsed_time()
            }
        
        return None

    def reveal_cell(self, row, col):
        """
        Reveal a cell at the specified position.
        
        Args:
            row (int): The row index.
            col (int): The column index.
            
        Returns:
            dict: Information about the revealed cells and game state.
        """
        # Cannot play if game is not in progress
        if self.game_state not in ['new', 'in_progress']:
            return False
        
        # Start the game if it's new
        if self.game_state == 'new':
            self.start_game()
        
        # Track revealed cells before the move
        revealed_before = set()
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.get_cell(r, c)
                if cell and cell.is_revealed:
                    revealed_before.add((r, c))
        
        # Reveal the cell
        result = self.board.reveal_cell(row, col)
        
        # If the result is False, return early
        if not result:
            return False
        
        # Track newly revealed cells and check win condition
        revealed_cells = []
        won = False
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.get_cell(r, c)
                if cell and cell.is_revealed and (r, c) not in revealed_before:
                    revealed_cells.append({
                        'row': r,
                        'col': c,
                        'is_mine': cell.is_mine,
                        'adjacent_mines': cell.adjacent_mines
                    })
        
        # Check for win/loss
        if self.board.game_state == 'lost':
            self.game_state = 'lost'
            self.elapsed_time = self.get_elapsed_time()
        elif self.board._check_win_condition():
            self.game_state = 'won'
            self.elapsed_time = self.get_elapsed_time()
            self.handle_win()
        
        # Return detailed information
        return {
            'game_state': self.game_state,
            'revealed_cells': revealed_cells,
            'mines_remaining': self.get_remaining_mines(),
            'elapsed_time': self.get_elapsed_time()
        }
    
    def toggle_flag(self, row, col):
        """
        Toggle a flag on a cell at the specified position.
        
        Args:
            row (int): The row index.
            col (int): The column index.
            
        Returns:
            dict: Information about the flagged cell and game state.
        """
        # Cannot play if game is not in progress
        if self.game_state not in ['new', 'in_progress']:
            return False
        
        # Start the game if it's new
        if self.game_state == 'new':
            self.start_game()
        
        # Get the cell
        cell = self.board.get_cell(row, col)
        if not cell:
            return False
        
        # Track the flag state before toggling
        was_flagged = cell.is_flagged
        
        # Toggle the flag
        result = self.board.toggle_flag(row, col)
        
        # Update flag count if the flag state changed
        if result:
            if was_flagged:
                self.flags_placed -= 1
            else:
                self.flags_placed += 1
        
        # If the result is False, return early
        if not result:
            return False
        
        # Return detailed information
        return {
            'game_state': self.game_state,
            'flagged_cell': {
                'row': row,
                'col': col,
                'is_flagged': cell.is_flagged
            },
            'mines_remaining': self.get_remaining_mines(),
            'elapsed_time': self.get_elapsed_time()
        }
    
    def handle_win(self):
        """Handle game win condition."""
        self.game_state = 'won'
        self.elapsed_time = self.get_elapsed_time()
    
    def add_high_score(self, player_name):
        """
        Add a new high score.
        
        Args:
            player_name (str): Name of the player.
            
        Returns:
            bool: True if the score was added, False otherwise.
        """
        if self.game_state == 'won':
            return self.high_score_manager.add_score(player_name, self.elapsed_time)
        return False
    
    def get_high_scores(self):
        """
        Get the list of high scores.
        
        Returns:
            list: List of high score entries.
        """
        scores = self.high_score_manager.get_scores()
        return [{'name': score.player_name, 'time': score.completion_time} for score in scores]
    

