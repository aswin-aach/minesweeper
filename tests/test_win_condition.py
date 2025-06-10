import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.board import Board
from src.controllers.game_controller import GameController

class TestWinCondition(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.board = Board(3, 3)  # Small board for testing
        self.controller = GameController(3, 3, 2)  # 3x3 board with 2 mines
        
    def test_win_condition(self):
        """Test that win condition is detected correctly"""
        # Start game (this will place random mines)
        self.controller.start_game()
        
        # Override the mine positions
        for row in range(3):
            for col in range(3):
                self.controller.board.grid[row][col].is_mine = False
        self.controller.board.grid[0][0].is_mine = True
        self.controller.board.grid[2][2].is_mine = True
        self.controller.board.calculate_adjacent_mines()
        
        # Reveal all non-mine cells
        cells_to_reveal = [(0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1)]
        for row, col in cells_to_reveal:
            result = self.controller.reveal_cell(row, col)
            self.assertIsNotNone(result, f"Failed to reveal cell at ({row}, {col})")
        
        # Check game state
        self.assertEqual(self.controller.game_state, 'won', "Game should be won after revealing all non-mine cells")
        
    def test_win_condition_with_flags(self):
        """Test that win condition works with flagged mines"""
        # Start game (this will place random mines)
        self.controller.start_game()
        
        # Override the mine positions
        for row in range(3):
            for col in range(3):
                self.controller.board.grid[row][col].is_mine = False
        self.controller.board.grid[0][0].is_mine = True
        self.controller.board.grid[2][2].is_mine = True
        self.controller.board.calculate_adjacent_mines()
        
        # Flag the mines
        self.controller.toggle_flag(0, 0)
        self.controller.toggle_flag(2, 2)
        
        # Reveal all non-mine cells
        cells_to_reveal = [(0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1)]
        for row, col in cells_to_reveal:
            result = self.controller.reveal_cell(row, col)
            self.assertIsNotNone(result, f"Failed to reveal cell at ({row}, {col})")
        
        # Check game state
        self.assertEqual(self.controller.game_state, 'won', "Game should be won after revealing all non-mine cells and flagging mines")

if __name__ == '__main__':
    unittest.main()
