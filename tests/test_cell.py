import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.cell import Cell


class TestCell(unittest.TestCase):
    def test_cell_initialization(self):
        """Test that a cell initializes with default values correctly"""
        cell = Cell(1, 2)
        
        self.assertEqual(cell.position, (1, 2))
        self.assertFalse(cell.is_mine)
        self.assertFalse(cell.is_revealed)
        self.assertFalse(cell.is_flagged)
        self.assertEqual(cell.adjacent_mines, 0)
    
    def test_cell_initialization_with_mine(self):
        """Test that a cell can be initialized with a mine"""
        cell = Cell(3, 4, is_mine=True)
        
        self.assertTrue(cell.is_mine)
        self.assertEqual(cell.position, (3, 4))
    
    def test_set_adjacent_mines(self):
        """Test setting the number of adjacent mines"""
        cell = Cell(0, 0)
        cell.adjacent_mines = 3
        
        self.assertEqual(cell.adjacent_mines, 3)
    
    def test_toggle_flag(self):
        """Test toggling the flag on a cell"""
        cell = Cell(5, 6)
        
        # Initially not flagged
        self.assertFalse(cell.is_flagged)
        
        # Toggle flag on
        cell.toggle_flag()
        self.assertTrue(cell.is_flagged)
        
        # Toggle flag off
        cell.toggle_flag()
        self.assertFalse(cell.is_flagged)
    
    def test_cannot_flag_revealed_cell(self):
        """Test that a revealed cell cannot be flagged"""
        cell = Cell(7, 8)
        cell.is_revealed = True
        
        cell.toggle_flag()
        self.assertFalse(cell.is_flagged)
    
    def test_reveal_cell(self):
        """Test revealing a cell"""
        cell = Cell(9, 10)
        
        # Initially not revealed
        self.assertFalse(cell.is_revealed)
        
        # Reveal the cell
        result = cell.reveal()
        self.assertTrue(cell.is_revealed)
        self.assertFalse(result)  # Not a mine, so return False
    
    def test_reveal_mine(self):
        """Test revealing a cell with a mine"""
        cell = Cell(11, 12, is_mine=True)
        
        result = cell.reveal()
        self.assertTrue(cell.is_revealed)
        self.assertTrue(result)  # Is a mine, so return True
    
    def test_cannot_reveal_flagged_cell(self):
        """Test that a flagged cell cannot be revealed"""
        cell = Cell(13, 14)
        cell.toggle_flag()
        
        before_reveal = cell.is_revealed
        cell.reveal()
        
        # Should remain unchanged
        self.assertEqual(cell.is_revealed, before_reveal)
    
    def test_str_representation(self):
        """Test the string representation of a cell"""
        cell = Cell(15, 16, is_mine=True)
        cell.adjacent_mines = 3
        
        # Should include position and mine status
        str_rep = str(cell)
        self.assertIn("(15, 16)", str_rep)
        self.assertIn("mine", str_rep.lower())


if __name__ == '__main__':
    unittest.main()
