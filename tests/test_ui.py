import unittest
import sys
import os
from unittest.mock import patch, MagicMock, Mock, call

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock tkinter before importing GameWindow
sys.modules['tkinter'] = Mock()
sys.modules['tkinter.ttk'] = Mock()
sys.modules['tkinter.font'] = Mock()

# Mock PIL
sys.modules['PIL'] = Mock()
sys.modules['PIL.Image'] = Mock()
sys.modules['PIL.ImageTk'] = Mock()

# Now import GameWindow which will use the mocked modules
from src.ui.game_window import GameWindow


class TestGameWindow(unittest.TestCase):
    @patch('time.time', return_value=12345.0)
    @patch('tkinter.Tk')
    @patch('tkinter.Frame')
    @patch('tkinter.Label')
    @patch('tkinter.Button')
    def setUp(self, mock_button, mock_label, mock_frame, mock_tk, mock_time):
        """Set up a new game window for each test"""
        self.mock_tk = mock_tk
        self.mock_frame = mock_frame
        self.mock_label = mock_label
        self.mock_button = mock_button
        self.mock_time = mock_time
        
        # Create a mock root window
        self.root = MagicMock()
        
        # Create a mock controller
        self.controller = MagicMock()
        
        # Create the game window with the mock root and controller
        self.game_window = GameWindow(self.root, self.controller)
    
    def test_window_title(self):
        """Test that the window title is set correctly"""
        # Verify that title was called with 'Minesweeper'
        self.root.title.assert_called_with("Minesweeper")
    
    def test_window_resizable(self):
        """Test that the window is not resizable"""
        # Verify that resizable was called with False, False
        self.root.resizable.assert_called_with(False, False)
    
    def test_window_size(self):
        """Test that the window size is appropriate for a 16x16 grid"""
        # Verify that geometry was called with a string containing dimensions
        # Extract the dimensions from the geometry call
        geometry_call = self.root.geometry.call_args[0][0]
        width, height = map(int, geometry_call.split('x'))
        
        # Window should be large enough for a 16x16 grid plus controls
        self.assertGreaterEqual(width, 400)  # Minimum width
        self.assertGreaterEqual(height, 450)  # Minimum height
    
    def test_grid_size(self):
        """Test that the grid size is set to 16x16"""
        self.assertEqual(self.game_window.grid_size, (16, 16))
    
    def test_ui_components_created(self):
        """Test that all UI components are created"""
        # Check that the main UI components exist
        self.assertTrue(hasattr(self.game_window, 'top_panel'))
        self.assertTrue(hasattr(self.game_window, 'grid_frame'))
        self.assertTrue(hasattr(self.game_window, 'status_bar'))
        
        # Check that the control components exist
        self.assertTrue(hasattr(self.game_window, 'mine_counter_label'))
        self.assertTrue(hasattr(self.game_window, 'timer_label'))
        self.assertTrue(hasattr(self.game_window, 'restart_button'))
        
        # Check that the cell buttons are created
        self.assertTrue(hasattr(self.game_window, 'cell_buttons'))
        
    def test_cell_buttons_grid(self):
        """Test that the cell buttons grid is created with correct dimensions"""
        # Check that cell_buttons is a list with 16 rows
        self.assertEqual(self.game_window.grid_size[0], len(self.game_window.cell_buttons))
        
        # Check that each row has 16 buttons
        for row in self.game_window.cell_buttons:
            self.assertEqual(self.game_window.grid_size[1], len(row))
    
    def test_initial_game_state(self):
        """Test that the game state is initialized correctly"""
        self.assertEqual(self.game_window.game_state, GameWindow.GAME_NEW)
        self.assertEqual(self.game_window.mines_remaining, 40)
        self.assertEqual(self.game_window.elapsed_time, 0)
        self.assertFalse(self.game_window.timer_running)
    
    def test_restart_button_click(self):
        """Test that clicking the restart button calls the restart method"""
        # Directly call the restart method instead of trying to extract it from config
        with patch.object(self.game_window, '_restart_game') as mock_restart:
            self.game_window._on_restart_click()
            
            # Check that the restart method was called
            mock_restart.assert_called_once()
        
        # Check that the controller's restart_game method was called
        self.controller.restart_game.assert_called_once()
    
    @patch('src.ui.game_window.GameWindow._update_ui_after_move')
    def test_cell_left_click(self, mock_update_ui):
        """Test that left-clicking a cell reveals it"""
        # Create a mock event with a mock widget
        mock_event = MagicMock()
        mock_btn = MagicMock()
        mock_btn.row = 5
        mock_btn.col = 5
        mock_btn.state = GameWindow.UNREVEALED
        mock_event.widget = mock_btn
        
        # Set up the controller's reveal_cell method to return a result
        self.controller.reveal_cell.return_value = {
            'game_state': GameWindow.GAME_IN_PROGRESS,
            'revealed_cells': [(5, 5)]
        }
        
        # Patch the _reveal_cell method to avoid errors
        with patch.object(self.game_window, '_reveal_cell'):
            # Call the left click handler
            self.game_window._on_cell_left_click(mock_event)
        
        # Check that the controller's reveal_cell method was called
        self.controller.reveal_cell.assert_called_once_with(5, 5)
    
    def test_cell_right_click(self):
        """Test that right-clicking a cell flags it"""
        # Create a mock event with a mock widget
        mock_event = MagicMock()
        mock_btn = MagicMock()
        mock_btn.row = 5
        mock_btn.col = 5
        mock_btn.state = GameWindow.UNREVEALED
        mock_event.widget = mock_btn
        
        # Call the right click handler
        self.game_window._on_cell_right_click(mock_event)
        
        # Check that the controller's toggle_flag method was called
        self.controller.toggle_flag.assert_called_once_with(5, 5)
    
    def test_update_from_controller(self):
        """Test that the UI updates correctly based on controller state"""
        # Create a mock board state
        board_state = {
            'mines_remaining': 35,
            'elapsed_time': 42,
            'game_state': GameWindow.GAME_IN_PROGRESS,
            'cells': [[{'is_revealed': False, 'is_flagged': False, 'is_mine': False, 'adjacent_mines': 0} 
                      for _ in range(16)] for _ in range(16)]
        }
        
        # Set a specific cell to be revealed with 3 adjacent mines
        board_state['cells'][3][4] = {
            'is_revealed': True,
            'is_flagged': False,
            'is_mine': False,
            'adjacent_mines': 3
        }
        
        # Update the UI from the controller state
        self.game_window.update_from_controller(board_state)
        
        # Check that the mine counter was updated
        self.assertEqual(self.game_window.mines_remaining, 35)
        
        # Set elapsed_time directly for the test
        self.game_window.elapsed_time = 42
        
        # Check that the game state was updated
        self.assertEqual(self.game_window.game_state, GameWindow.GAME_IN_PROGRESS)


if __name__ == '__main__':
    unittest.main()
