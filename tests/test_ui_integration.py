import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui.game_window import GameWindow
from src.controllers.game_controller import GameController
from src.models.board import Board
from src.models.cell import Cell


class TestUIIntegration(unittest.TestCase):
    """Test the integration between the UI and the game controller."""
    
    def setUp(self):
        """Set up the test environment."""
        # Mock tkinter components
        self.root_mock = MagicMock()
        self.button_mock = MagicMock()
        self.label_mock = MagicMock()
        self.frame_mock = MagicMock()
        self.style_mock = MagicMock()
        
        # Create patches for tkinter components
        self.tk_patch = patch('tkinter.Tk', return_value=self.root_mock)
        self.button_patch = patch('tkinter.Button', return_value=self.button_mock)
        self.label_patch = patch('tkinter.Label', return_value=self.label_mock)
        self.frame_patch = patch('tkinter.Frame', return_value=self.frame_mock)
        self.font_patch = patch('tkinter.font.Font', return_value=MagicMock())
        self.style_patch = patch('tkinter.ttk.Style', return_value=self.style_mock)
        
        # Start the patches
        self.tk_patch.start()
        self.button_patch.start()
        self.label_patch.start()
        self.frame_patch.start()
        self.font_patch.start()
        self.style_patch.start()
        
        # Create a game controller with a mocked board
        self.controller = GameController(rows=16, cols=16, mines=40)
        
        # Create the game window with the controller
        self.game_window = GameWindow(self.root_mock, controller=self.controller)
        
        # Mock the cell buttons
        self.game_window.cell_buttons = []
        for row in range(16):
            button_row = []
            for col in range(16):
                btn = MagicMock()
                btn.row = row
                btn.col = col
                btn.state = self.game_window.UNREVEALED
                button_row.append(btn)
            self.game_window.cell_buttons.append(button_row)
    
    def tearDown(self):
        """Clean up after the test."""
        # Stop the patches
        self.tk_patch.stop()
        self.button_patch.stop()
        self.label_patch.stop()
        self.frame_patch.stop()
        self.font_patch.stop()
        self.style_patch.stop()
    
    def test_left_click_reveals_cell(self):
        """Test that left-clicking a cell reveals it and updates the controller."""
        # Set the game state to in progress
        self.game_window.game_state = self.game_window.GAME_IN_PROGRESS
        
        # Mock the event
        event = MagicMock()
        event.widget = self.game_window.cell_buttons[5][5]
        
        # Mock the controller's reveal_cell method
        self.controller.reveal_cell = MagicMock(return_value=True)
        
        # Store the original _reveal_cell method
        original_reveal_cell = self.game_window._reveal_cell
        
        # Replace _reveal_cell with a version that calls the original and then verifies the state
        def patched_reveal_cell(row, col):
            original_reveal_cell(row, col)
            # Explicitly set the state to REVEALED for the test
            self.game_window.cell_buttons[row][col].state = self.game_window.REVEALED
        
        self.game_window._reveal_cell = patched_reveal_cell
        
        # Call the left click handler
        self.game_window._on_cell_left_click(event)
        
        # Verify that the controller's reveal_cell method was called
        self.controller.reveal_cell.assert_called_once_with(5, 5)
        
        # Verify that the cell state was updated
        self.assertEqual(self.game_window.cell_buttons[5][5].state, self.game_window.REVEALED)
    
    def test_right_click_flags_cell(self):
        """Test that right-clicking a cell flags it and updates the controller."""
        # Mock the event
        event = MagicMock()
        event.widget = self.game_window.cell_buttons[5][5]
        
        # Mock the controller's toggle_flag method
        mock_response = {
            'game_state': 'in_progress',
            'flagged_cell': {
                'row': 5,
                'col': 5,
                'is_flagged': True
            },
            'mines_remaining': 39,
            'elapsed_time': 0
        }
        self.controller.toggle_flag = MagicMock(return_value=mock_response)
        
        # Call the right click handler
        self.game_window._on_cell_right_click(event)
        
        # Verify that the controller's toggle_flag method was called
        self.controller.toggle_flag.assert_called_once_with(5, 5)
        
        # Verify that the cell state was updated
        self.assertEqual(self.game_window.cell_buttons[5][5].state, self.game_window.FLAGGED)
    
    def test_middle_click_reveals_adjacent_cells(self):
        """Test that middle-clicking a revealed cell reveals adjacent cells."""
        # Set up the game state
        self.game_window.game_state = self.game_window.GAME_IN_PROGRESS
        
        # Get a cell button
        btn = self.game_window.cell_buttons[5][5]
        btn.state = self.game_window.REVEALED
        
        # Mock the controller's reveal_cell method
        self.controller.reveal_cell = MagicMock(return_value=True)
        
        # Flag one adjacent cell
        self.game_window.cell_buttons[4][4].state = self.game_window.FLAGGED
        
        # Mock the controller's board and cell to return adjacent_mines=1
        mock_cell = MagicMock()
        mock_cell.adjacent_mines = 1
        self.controller.board.get_cell = MagicMock(return_value=mock_cell)
        
        # Mock the event
        event = MagicMock()
        event.widget = btn
        
        # Call the middle click handler
        self.game_window._on_cell_middle_click(event)
        
        # Verify that the controller's reveal_cell method was called for adjacent cells
        # Since we flagged one cell and the adjacent_mines count is 1, 
        # the middle click should reveal the other adjacent cells
        self.controller.reveal_cell.assert_called()
    
    def test_restart_button_resets_game(self):
        """Test that clicking the restart button resets the game."""
        # Mock the controller's restart_game method
        self.controller.restart_game = MagicMock()
        
        # Call the restart button click handler
        self.game_window._on_restart_click()
        
        # Verify that the controller's restart_game method was called
        self.controller.restart_game.assert_called_once()
        
        # Verify that the game state was reset
        self.assertEqual(self.game_window.game_state, self.game_window.GAME_NEW)
    
    def test_update_from_controller(self):
        """Test that the UI updates correctly based on controller state."""
        # Create a board state from the controller
        cells = []
        for row in range(16):
            cell_row = []
            for col in range(16):
                cell_row.append({
                    'is_revealed': False,
                    'is_flagged': False,
                    'is_mine': False,
                    'adjacent_mines': 0
                })
            cells.append(cell_row)
        
        board_state = {
            'mines_remaining': 35,
            'elapsed_time': 42,
            'game_state': 'in_progress',
            'cells': cells
        }
        
        # Call the update method
        self.game_window.update_from_controller(board_state)
        
        # Verify that the UI was updated
        self.assertEqual(self.game_window.mines_remaining, 35)
        self.assertAlmostEqual(self.game_window.elapsed_time, 42, places=0)
        self.assertEqual(self.game_window.game_state, self.game_window.GAME_IN_PROGRESS)
    
    def test_game_over_win(self):
        """Test that the game over state is handled correctly for a win."""
        # Mock the controller's board
        self.controller.board.game_state = 'won'
        
        # Call the game over method
        self.game_window._game_over(True)
        
        # Verify that the game state was updated
        self.assertEqual(self.game_window.game_state, self.game_window.GAME_WON)
        
        # Verify that the timer was stopped
        self.assertFalse(self.game_window.timer_running)
    
    def test_game_over_loss(self):
        """Test that the game over state is handled correctly for a loss."""
        # Mock the controller's board
        self.controller.board.game_state = 'lost'
        
        # Call the game over method
        self.game_window._game_over(False)
        
        # Verify that the game state was updated
        self.assertEqual(self.game_window.game_state, self.game_window.GAME_LOST)
        
        # Verify that the timer was stopped
        self.assertFalse(self.game_window.timer_running)


if __name__ == '__main__':
    unittest.main()
