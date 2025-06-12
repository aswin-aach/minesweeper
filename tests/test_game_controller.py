import unittest
import sys
import os
import time
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.board import Board
from src.models.cell import Cell
from src.controllers.game_controller import GameController


class TestGameController(unittest.TestCase):
    def setUp(self):
        """Set up a new game controller for each test"""
        self.game_controller = GameController()
    
    def test_initialization(self):
        """Test that the game controller initializes correctly"""
        # Board should be initialized
        self.assertIsInstance(self.game_controller.board, Board)
        
        # Game state should be 'new'
        self.assertEqual(self.game_controller.game_state, 'new')
        
        # Timer should be at 0
        self.assertEqual(self.game_controller.elapsed_time, 0)
        
        # Mines should be 40
        self.assertEqual(self.game_controller.total_mines, 40)
        
        # Flags should be 0
        self.assertEqual(self.game_controller.flags_placed, 0)
    
    def test_start_game(self):
        """Test starting a new game"""
        self.game_controller.start_game()
        
        # Game state should be 'in_progress'
        self.assertEqual(self.game_controller.game_state, 'in_progress')
        
        # Board should have mines placed
        mine_count = sum(1 for row in self.game_controller.board.grid 
                         for cell in row if cell.is_mine)
        self.assertEqual(mine_count, 40)
    
    @patch('time.time')
    def test_timer_functionality(self, mock_time):
        """Test that the timer works correctly"""
        # Mock time.time to return controlled values
        mock_time.return_value = 100
        
        # Start the game
        self.game_controller.start_game()
        self.game_controller.start_time = 100  # Explicitly set start time
        
        # Check initial time
        mock_time.return_value = 100
        self.assertEqual(self.game_controller.get_elapsed_time(), 0)
        
        # Check time after 5 seconds
        mock_time.return_value = 105
        self.assertEqual(self.game_controller.get_elapsed_time(), 5)
        
        # Check time after 10 seconds
        mock_time.return_value = 110
        self.assertEqual(self.game_controller.get_elapsed_time(), 10)
    
    def test_flag_counting(self):
        """Test that flag counting works correctly"""
        # Start the game
        self.game_controller.start_game()
        
        # Initially, no flags are placed
        self.assertEqual(self.game_controller.flags_placed, 0)
        self.assertEqual(self.game_controller.get_remaining_mines(), 40)
        
        # Place a flag
        self.game_controller.toggle_flag(5, 5)
        self.assertEqual(self.game_controller.flags_placed, 1)
        self.assertEqual(self.game_controller.get_remaining_mines(), 39)
        
        # Remove the flag
        self.game_controller.toggle_flag(5, 5)
        self.assertEqual(self.game_controller.flags_placed, 0)
        self.assertEqual(self.game_controller.get_remaining_mines(), 40)
    
    def test_reveal_cell(self):
        """Test revealing a cell"""
        # Start the game
        self.game_controller.start_game()
        
        # Force a cell to not be a mine
        self.game_controller.board.grid[5][5].is_mine = False
        
        # Reveal the cell
        self.game_controller.reveal_cell(5, 5)
        
        # The cell should be revealed
        self.assertTrue(self.game_controller.board.grid[5][5].is_revealed)
    
    def test_game_over_on_mine(self):
        """Test that the game ends when a mine is revealed"""
        # Start the game
        self.game_controller.start_game()
        
        # Force a cell to be a mine
        self.game_controller.board.grid[5][5].is_mine = True
        
        # Reveal the cell with the mine
        self.game_controller.reveal_cell(5, 5)
        
        # Game should be lost
        self.assertEqual(self.game_controller.game_state, 'lost')
    
    def test_game_won(self):
        """Test that the game is won when all non-mine cells are revealed"""
        # Create a small test board with known mine positions
        self.game_controller = GameController(rows=3, cols=3, mines=1)
        self.game_controller.start_game()
        
        # Force the mine to be at a specific position
        for row in range(3):
            for col in range(3):
                self.game_controller.board.grid[row][col].is_mine = False
        self.game_controller.board.grid[0][0].is_mine = True
        self.game_controller.board.calculate_adjacent_mines()
        
        # Reveal all non-mine cells
        for row in range(3):
            for col in range(3):
                if not (row == 0 and col == 0):  # Skip the mine
                    self.game_controller.reveal_cell(row, col)
        
        # Game should be won
        self.assertEqual(self.game_controller.game_state, 'won')
    
    def test_restart_game(self):
        """Test restarting the game"""
        # Start and play a bit
        self.game_controller.start_game()
        self.game_controller.reveal_cell(5, 5)
        self.game_controller.toggle_flag(10, 10)
        
        # Restart the game
        self.game_controller.restart_game()
        
        # Game state should be 'new'
        self.assertEqual(self.game_controller.game_state, 'new')
        
        # Timer should be reset
        self.assertEqual(self.game_controller.elapsed_time, 0)
        
        # Flags should be reset
        self.assertEqual(self.game_controller.flags_placed, 0)
        
        # Board should be reset (no revealed cells or flags)
        for row in self.game_controller.board.grid:
            for cell in row:
                self.assertFalse(cell.is_revealed)
                self.assertFalse(cell.is_flagged)
    
    def test_high_score_tracking(self):
        """Test high score tracking functionality"""
        # Clear existing high scores
        if self.game_controller.high_score_manager.scores_file.exists():
            self.game_controller.high_score_manager.scores_file.unlink()
        
        # Set up a game with a fixed elapsed time
        self.game_controller.elapsed_time = 100
        self.game_controller.game_state = 'won'  # Must be in won state to add score
        
        # Add a high score
        self.game_controller.add_high_score("Player1")
        
        # Check that the high score was added
        high_scores = self.game_controller.get_high_scores()
        self.assertEqual(len(high_scores), 1)
        self.assertEqual(high_scores[0]['name'], "Player1")
        self.assertEqual(high_scores[0]['time'], 100)
    
    def test_cannot_play_after_game_over(self):
        """Test that cells cannot be revealed after the game is over"""
        # Start the game
        self.game_controller.start_game()
        
        # Force a cell to be a mine and reveal it to end the game
        self.game_controller.board.grid[5][5].is_mine = True
        self.game_controller.reveal_cell(5, 5)
        
        # Try to reveal another cell
        self.game_controller.reveal_cell(10, 10)
        
        # The cell should not be revealed
        self.assertFalse(self.game_controller.board.grid[10][10].is_revealed)


if __name__ == '__main__':
    unittest.main()
