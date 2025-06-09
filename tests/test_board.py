import unittest
import sys
import os
import random

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.board import Board
from src.models.cell import Cell


class TestBoard(unittest.TestCase):
    def setUp(self):
        """Set up a new board for each test"""
        # Use a fixed seed for deterministic tests
        random.seed(42)
        self.board = Board()
    
    def test_board_initialization(self):
        """Test that the board initializes with correct dimensions"""
        # Board should be 16x16
        self.assertEqual(len(self.board.grid), 16)
        for row in self.board.grid:
            self.assertEqual(len(row), 16)
        
        # Each cell should be a Cell object with correct position
        for row_idx, row in enumerate(self.board.grid):
            for col_idx, cell in enumerate(row):
                self.assertIsInstance(cell, Cell)
                self.assertEqual(cell.position, (row_idx, col_idx))
        
        # Initially, no mines should be placed
        mine_count = sum(1 for row in self.board.grid for cell in row if cell.is_mine)
        self.assertEqual(mine_count, 0)
        
        # Game state should be 'new'
        self.assertEqual(self.board.game_state, 'new')
    
    def test_place_mines(self):
        """Test that mines are placed correctly"""
        self.board.place_mines(40)
        
        # Count mines
        mine_count = sum(1 for row in self.board.grid for cell in row if cell.is_mine)
        self.assertEqual(mine_count, 40)
        
        # Check that mines are placed at different positions
        mine_positions = [(row_idx, col_idx) 
                          for row_idx, row in enumerate(self.board.grid) 
                          for col_idx, cell in enumerate(row) 
                          if cell.is_mine]
        self.assertEqual(len(mine_positions), 40)
        self.assertEqual(len(set(mine_positions)), 40)  # No duplicates
    
    def test_calculate_adjacent_mines(self):
        """Test that adjacent mine counts are calculated correctly"""
        # Place mines at known positions
        self.board = Board()
        
        # Place a mine at (5, 5)
        self.board.grid[5][5].is_mine = True
        
        # Calculate adjacent mines
        self.board.calculate_adjacent_mines()
        
        # Check adjacent cells
        for row_idx in range(4, 7):
            for col_idx in range(4, 7):
                if (row_idx, col_idx) == (5, 5):
                    # Skip the mine itself
                    continue
                self.assertEqual(self.board.grid[row_idx][col_idx].adjacent_mines, 1)
        
        # Check a cell that's not adjacent to any mine
        self.assertEqual(self.board.grid[0][0].adjacent_mines, 0)
    
    def test_reveal_cell_with_mine(self):
        """Test that revealing a cell with a mine ends the game"""
        # Place a mine at (3, 3)
        self.board.grid[3][3].is_mine = True
        
        # Reveal the cell with the mine
        self.board.reveal_cell(3, 3)
        
        # Game should be lost
        self.assertEqual(self.board.game_state, 'lost')
        
        # The mine should be revealed
        self.assertTrue(self.board.grid[3][3].is_revealed)
    
    def test_reveal_cell_with_number(self):
        """Test that revealing a numbered cell only reveals that cell"""
        # Place a mine at (3, 3)
        self.board.grid[3][3].is_mine = True
        
        # Calculate adjacent mines
        self.board.calculate_adjacent_mines()
        
        # Reveal a cell adjacent to the mine
        self.board.reveal_cell(2, 2)
        
        # Only that cell should be revealed
        self.assertTrue(self.board.grid[2][2].is_revealed)
        
        # Count total revealed cells
        revealed_count = sum(1 for row in self.board.grid for cell in row if cell.is_revealed)
        self.assertEqual(revealed_count, 1)
    
    def test_reveal_cell_with_zero_adjacent_mines(self):
        """Test that revealing an empty cell reveals neighboring cells recursively"""
        # Place a mine at (15, 15) far from where we'll reveal
        self.board.grid[15][15].is_mine = True
        
        # Calculate adjacent mines
        self.board.calculate_adjacent_mines()
        
        # Reveal a cell with no adjacent mines
        self.board.reveal_cell(0, 0)
        
        # Multiple cells should be revealed due to flood fill
        revealed_count = sum(1 for row in self.board.grid for cell in row if cell.is_revealed)
        self.assertGreater(revealed_count, 1)
    
    def test_flag_cell(self):
        """Test flagging a cell"""
        # Flag a cell
        self.board.toggle_flag(5, 5)
        
        # The cell should be flagged
        self.assertTrue(self.board.grid[5][5].is_flagged)
        
        # Unflag the cell
        self.board.toggle_flag(5, 5)
        
        # The cell should not be flagged
        self.assertFalse(self.board.grid[5][5].is_flagged)
    
    def test_cannot_reveal_flagged_cell(self):
        """Test that a flagged cell cannot be revealed"""
        # Flag a cell
        self.board.toggle_flag(5, 5)
        
        # Try to reveal the flagged cell
        self.board.reveal_cell(5, 5)
        
        # The cell should not be revealed
        self.assertFalse(self.board.grid[5][5].is_revealed)
    
    def test_win_condition(self):
        """Test that the game is won when all non-mine cells are revealed"""
        # Place a mine
        self.board.grid[0][0].is_mine = True
        
        # Calculate adjacent mines
        self.board.calculate_adjacent_mines()
        
        # Reveal all non-mine cells
        for row_idx, row in enumerate(self.board.grid):
            for col_idx, cell in enumerate(row):
                if not cell.is_mine:
                    self.board.reveal_cell(row_idx, col_idx)
        
        # Game should be won
        self.assertEqual(self.board.game_state, 'won')
    
    def test_get_cell(self):
        """Test getting a cell by coordinates"""
        cell = self.board.get_cell(5, 5)
        self.assertIsInstance(cell, Cell)
        self.assertEqual(cell.position, (5, 5))
    
    def test_get_cell_out_of_bounds(self):
        """Test getting a cell with out-of-bounds coordinates"""
        cell = self.board.get_cell(-1, 5)
        self.assertIsNone(cell)
        
        cell = self.board.get_cell(5, 16)
        self.assertIsNone(cell)
    
    def test_get_neighbors(self):
        """Test getting neighboring cells"""
        # Get neighbors of a corner cell (should have 3 neighbors)
        neighbors = self.board.get_neighbors(0, 0)
        self.assertEqual(len(neighbors), 3)
        
        # Get neighbors of an edge cell (should have 5 neighbors)
        neighbors = self.board.get_neighbors(0, 5)
        self.assertEqual(len(neighbors), 5)
        
        # Get neighbors of a middle cell (should have 8 neighbors)
        neighbors = self.board.get_neighbors(5, 5)
        self.assertEqual(len(neighbors), 8)


if __name__ == '__main__':
    unittest.main()
