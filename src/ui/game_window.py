import tkinter as tk
from tkinter import ttk, font
import os
import sys
from PIL import Image, ImageTk
import time

# Add the src directory to the Python path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class GameWindow:
    """
    Main window for the Minesweeper game.
    
    This class handles the UI layout and components.
    """
    
    # Cell states
    UNREVEALED = 0
    REVEALED = 1
    FLAGGED = 2
    QUESTION = 3  # Optional state for question mark
    
    # Game states
    GAME_NEW = 'new'
    GAME_IN_PROGRESS = 'in_progress'
    GAME_WON = 'won'
    GAME_LOST = 'lost'
    
    # Cell size in pixels
    CELL_SIZE = 25
    
    def __init__(self, root=None, controller=None):
        """
        Initialize the game window.
        
        Args:
            root (tk.Tk, optional): Root Tkinter window. If None, a new one is created.
            controller: Game controller instance (optional)
        """
        # Initialize the root window if not provided
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root
            
        # Store controller reference
        self.controller = controller
        
        # Set window properties
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')  # Windows 7 background color
        
        # Set window size for a 16x16 grid
        # Each cell is approximately 25x25 pixels
        # Add extra space for the top panel and borders
        window_width = 16 * self.CELL_SIZE + 20  # 16 cells * 25 pixels + padding
        window_height = 16 * self.CELL_SIZE + 80  # 16 cells * 25 pixels + top panel + padding
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Set grid size
        self.grid_size = (16, 16)
        
        # Initialize game state variables
        self.game_state = self.GAME_NEW
        self.mines_remaining = 40  # Default mine count
        self.elapsed_time = 0
        self.timer_running = False
        self.last_time_update = 0
        
        # Store cell images
        self.cell_images = {}
        
        # Create UI components
        self._create_widgets()
        self._create_cell_images()
        
        # Apply Windows 7 style
        self._apply_windows7_style()
    
    def _create_widgets(self):
        """Create and arrange all UI widgets."""
        # Create top panel frame
        self.top_panel = tk.Frame(self.root, bg='#f0f0f0', height=60)
        self.top_panel.pack(fill=tk.X, padx=10, pady=10)
        
        # Create mine counter (left side)
        self.mine_counter_frame = tk.Frame(self.top_panel, bg='#f0f0f0', width=80, height=40)
        self.mine_counter_frame.pack(side=tk.LEFT, padx=5)
        
        # Use a digital-looking font for the counter
        digital_font = font.Font(family="Courier", size=20, weight="bold")
        self.mine_counter_label = tk.Label(
            self.mine_counter_frame, 
            text=f"{self.mines_remaining:03d}", 
            font=digital_font, 
            bg='black', 
            fg='red',
            width=3
        )
        self.mine_counter_label.pack(pady=5)
        
        # Create restart button (center)
        self.restart_button_frame = tk.Frame(self.top_panel, bg='#f0f0f0')
        self.restart_button_frame.pack(side=tk.LEFT, expand=True, padx=5)
        
        # Create restart button with smiley face
        self.restart_button = tk.Button(
            self.restart_button_frame, 
            text="😊", 
            font=("Arial", 16), 
            width=2, 
            height=1,
            command=self._on_restart_click
        )
        self.restart_button.pack(pady=5)
        
        # Bind mouse events to change smiley face
        self.restart_button.bind("<ButtonPress-1>", self._on_restart_button_press)
        self.restart_button.bind("<ButtonRelease-1>", self._on_restart_button_release)
        
        # Create timer (right side)
        self.timer_frame = tk.Frame(self.top_panel, bg='#f0f0f0', width=80, height=40)
        self.timer_frame.pack(side=tk.RIGHT, padx=5)
        
        # Use the same digital font for the timer
        self.timer_label = tk.Label(
            self.timer_frame, 
            text="000", 
            font=digital_font, 
            bg='black', 
            fg='red',
            width=3
        )
        self.timer_label.pack(pady=5)
        
        # Create game grid frame
        self.grid_frame = tk.Frame(self.root, bg='#c0c0c0', bd=2, relief=tk.SUNKEN)
        self.grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a status bar
        self.status_bar = tk.Frame(self.root, bg='#f0f0f0', height=20)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = tk.Label(self.status_bar, text="Ready. Left-click to reveal, right-click to flag.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X)
        
        # Create grid cells
        self._create_grid_cells()
    
    def _create_grid_cells(self):
        """Create interactive buttons for the grid cells."""
        self.cell_buttons = []
        
        for row in range(self.grid_size[0]):
            button_row = []
            for col in range(self.grid_size[1]):
                # Create a button for each cell with raised appearance
                btn = tk.Button(
                    self.grid_frame, 
                    width=2, 
                    height=1, 
                    relief=tk.RAISED,
                    borderwidth=2,
                    bg='#c0c0c0'
                )
                
                # Store the cell coordinates as button attributes
                btn.row = row
                btn.col = col
                btn.state = self.UNREVEALED
                
                # Bind mouse events
                btn.bind("<Button-1>", self._on_cell_left_click)  # Left click
                btn.bind("<Button-3>", self._on_cell_right_click)  # Right click
                
                # Position the button in the grid
                btn.grid(row=row, column=col, padx=0, pady=0)
                button_row.append(btn)
            
            self.cell_buttons.append(button_row)
    
    def _on_cell_left_click(self, event):
        """Handle left click on a cell (reveal)."""
        # Get the button that was clicked
        btn = event.widget
        row, col = btn.row, btn.col
        
        # Update status
        self.status_label.config(text=f"Cell clicked: ({row}, {col})")
        
        # Change smiley face to 'pressed' state
        self.restart_button.config(text="😮")
        
        # Start the game if it's the first click
        if self.game_state == self.GAME_NEW:
            self.game_state = self.GAME_IN_PROGRESS
            self._start_timer()
            
            # If controller exists, notify it
            if self.controller:
                self.controller.start_game(row, col)
        
        # If the game is in progress and the cell is not flagged
        if self.game_state == self.GAME_IN_PROGRESS and btn.state != self.FLAGGED:
            # Reveal the cell
            self._reveal_cell(row, col)
            
            # If controller exists, notify it
            if self.controller:
                result = self.controller.reveal_cell(row, col)
                self._update_ui_after_move(result)
        
        # Reset smiley face after a short delay
        self.root.after(100, lambda: self.restart_button.config(text="😊"))
    
    def _on_cell_right_click(self, event):
        """Handle right click on a cell (flag)."""
        # Get the button that was clicked
        btn = event.widget
        row, col = btn.row, btn.col
        
        # Update status
        self.status_label.config(text=f"Cell flagged: ({row}, {col})")
        
        # Only allow flagging if the game is in progress and the cell is not revealed
        if self.game_state in [self.GAME_NEW, self.GAME_IN_PROGRESS] and btn.state != self.REVEALED:
            # Start the game if it's the first action
            if self.game_state == self.GAME_NEW:
                self.game_state = self.GAME_IN_PROGRESS
                self._start_timer()
            
            # Toggle flag state
            if btn.state == self.UNREVEALED:
                btn.state = self.FLAGGED
                btn.config(text="🚩", bg='#c0c0c0')
                self.mines_remaining -= 1
            else:  # Must be FLAGGED
                btn.state = self.UNREVEALED
                btn.config(text="", bg='#c0c0c0')
                self.mines_remaining += 1
            
            # Update mine counter
            self.mine_counter_label.config(text=f"{self.mines_remaining:03d}")
            
            # If controller exists, notify it
            if self.controller:
                self.controller.toggle_flag(row, col)
    
    def _on_restart_click(self):
        """Handle click on the restart button."""
        self.status_label.config(text="Game restarted")
        self._restart_game()
        
        # If controller exists, notify it
        if self.controller:
            self.controller.restart_game()
    
    def _on_restart_button_press(self, event):
        """Change smiley face when restart button is pressed."""
        self.restart_button.config(text="😮")
    
    def _on_restart_button_release(self, event):
        """Change smiley face back when restart button is released."""
        self.restart_button.config(text="😊")
    
    def _create_cell_images(self):
        """Create images for different cell states."""
        # For now, we'll use text-based representation instead of images
        # This can be enhanced later with actual image assets
        self.cell_images = {
            'unrevealed': {'text': '', 'bg': '#c0c0c0', 'relief': tk.RAISED},
            'flagged': {'text': '🚩', 'bg': '#c0c0c0', 'relief': tk.RAISED},
            'question': {'text': '?', 'bg': '#c0c0c0', 'relief': tk.RAISED},
            'mine': {'text': '💣', 'bg': '#ff0000', 'relief': tk.SUNKEN},  # Red background for exploded mine
            'mine_wrong': {'text': '❌', 'bg': '#c0c0c0', 'relief': tk.SUNKEN},  # Wrong flag
            'revealed': {'text': '', 'bg': '#e0e0e0', 'relief': tk.SUNKEN},
            '1': {'text': '1', 'bg': '#e0e0e0', 'fg': 'blue', 'relief': tk.SUNKEN},
            '2': {'text': '2', 'bg': '#e0e0e0', 'fg': 'green', 'relief': tk.SUNKEN},
            '3': {'text': '3', 'bg': '#e0e0e0', 'fg': 'red', 'relief': tk.SUNKEN},
            '4': {'text': '4', 'bg': '#e0e0e0', 'fg': 'darkblue', 'relief': tk.SUNKEN},
            '5': {'text': '5', 'bg': '#e0e0e0', 'fg': 'darkred', 'relief': tk.SUNKEN},
            '6': {'text': '6', 'bg': '#e0e0e0', 'fg': 'teal', 'relief': tk.SUNKEN},
            '7': {'text': '7', 'bg': '#e0e0e0', 'fg': 'black', 'relief': tk.SUNKEN},
            '8': {'text': '8', 'bg': '#e0e0e0', 'fg': 'gray', 'relief': tk.SUNKEN},
        }
    
    def _reveal_cell(self, row, col):
        """Reveal a cell at the given coordinates."""
        # Get the button at the specified coordinates
        btn = self.cell_buttons[row][col]
        
        # If the cell is already revealed or flagged, do nothing
        if btn.state == self.REVEALED or btn.state == self.FLAGGED:
            return
        
        # Mark the cell as revealed
        btn.state = self.REVEALED
        
        # For now, just change the appearance to 'revealed'
        # In a real implementation, we would check the cell content
        btn.config(
            relief=tk.SUNKEN,
            bg='#e0e0e0',
            text=''
        )
        
        # If controller exists, get the cell value
        if self.controller:
            cell = self.controller.board.get_cell(row, col)
            
            if cell.is_mine:
                # Show mine
                btn.config(
                    text='💣',
                    bg='#ff0000'  # Red background for exploded mine
                )
                self._game_over(False)  # Lost
            elif cell.adjacent_mines > 0:
                # Show number
                style = self.cell_images[str(cell.adjacent_mines)]
                btn.config(
                    text=str(cell.adjacent_mines),
                    fg=style['fg'],
                    bg=style['bg']
                )
            else:
                # Empty cell, could trigger flood fill
                pass
    
    def _update_ui_after_move(self, result):
        """Update UI based on the result of a move."""
        if not result:
            return
        
        # Update game state if needed
        if result.get('game_state'):
            self.game_state = result['game_state']
            
            if self.game_state == self.GAME_WON:
                self._game_over(True)  # Won
            elif self.game_state == self.GAME_LOST:
                self._game_over(False)  # Lost
        
        # Update revealed cells
        if result.get('revealed_cells'):
            for row, col in result['revealed_cells']:
                cell = self.controller.board.get_cell(row, col)
                btn = self.cell_buttons[row][col]
                
                # Mark as revealed
                btn.state = self.REVEALED
                
                if cell.adjacent_mines > 0:
                    # Show number
                    style = self.cell_images[str(cell.adjacent_mines)]
                    btn.config(
                        text=str(cell.adjacent_mines),
                        fg=style['fg'],
                        bg=style['bg'],
                        relief=tk.SUNKEN
                    )
                else:
                    # Empty cell
                    btn.config(
                        text='',
                        bg='#e0e0e0',
                        relief=tk.SUNKEN
                    )
    
    def _start_timer(self):
        """Start the game timer."""
        if not self.timer_running:
            self.timer_running = True
            self.last_time_update = time.time()
            self._update_timer()
    
    def _stop_timer(self):
        """Stop the game timer."""
        self.timer_running = False
    
    def _update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            current_time = time.time()
            self.elapsed_time += current_time - self.last_time_update
            self.last_time_update = current_time
            
            # Update the timer label (cap at 999 seconds)
            seconds = min(int(self.elapsed_time), 999)
            self.timer_label.config(text=f"{seconds:03d}")
            
            # Schedule the next update
            self.root.after(1000, self._update_timer)
    
    def _game_over(self, won):
        """Handle game over state."""
        self._stop_timer()
        
        if won:
            # Game won
            self.game_state = self.GAME_WON
            self.restart_button.config(text="😎")  # Cool face with sunglasses
            self.status_label.config(text="Game won! Congratulations!")
        else:
            # Game lost
            self.game_state = self.GAME_LOST
            self.restart_button.config(text="😵")  # Dizzy face
            self.status_label.config(text="Game over! You hit a mine.")
            
            # Reveal all mines
            self._reveal_all_mines()
    
    def _reveal_all_mines(self):
        """Reveal all mines on the board."""
        if not self.controller:
            return
            
        # Iterate through all cells
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                cell = self.controller.board.get_cell(row, col)
                btn = self.cell_buttons[row][col]
                
                if cell.is_mine:
                    # Show mine
                    if btn.state != self.FLAGGED:
                        btn.config(
                            text='💣',
                            bg='#c0c0c0',
                            relief=tk.SUNKEN
                        )
                elif btn.state == self.FLAGGED:
                    # Show wrongly flagged cell
                    btn.config(
                        text='❌',
                        bg='#c0c0c0',
                        relief=tk.SUNKEN
                    )
    
    def _restart_game(self):
        """Restart the game."""
        # Reset game state
        self.game_state = self.GAME_NEW
        self.mines_remaining = 40
        self.elapsed_time = 0
        self._stop_timer()
        
        # Reset UI
        self.mine_counter_label.config(text=f"{self.mines_remaining:03d}")
        self.timer_label.config(text="000")
        self.restart_button.config(text="😊")  # Normal smiley
        self.status_label.config(text="Ready. Left-click to reveal, right-click to flag.")
        
        # Reset all cell buttons
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                btn = self.cell_buttons[row][col]
                btn.state = self.UNREVEALED
                btn.config(
                    text='',
                    bg='#c0c0c0',
                    relief=tk.RAISED,
                    fg='black'  # Reset text color
                )
    
    def update_from_controller(self, board_state):
        """Update UI based on the controller's board state."""
        if not board_state:
            return
            
        # Update mine counter
        if 'mines_remaining' in board_state:
            self.mines_remaining = board_state['mines_remaining']
            self.mine_counter_label.config(text=f"{self.mines_remaining:03d}")
        
        # Update timer
        if 'elapsed_time' in board_state:
            self.elapsed_time = board_state['elapsed_time']
            seconds = min(int(self.elapsed_time), 999)
            self.timer_label.config(text=f"{seconds:03d}")
        
        # Update game state
        if 'game_state' in board_state:
            self.game_state = board_state['game_state']
            
            if self.game_state == self.GAME_WON:
                self.restart_button.config(text="😎")  # Cool face with sunglasses
                self.status_label.config(text="Game won! Congratulations!")
                self._stop_timer()
            elif self.game_state == self.GAME_LOST:
                self.restart_button.config(text="😵")  # Dizzy face
                self.status_label.config(text="Game over! You hit a mine.")
                self._stop_timer()
        
        # Update cell states
        if 'cells' in board_state:
            for row in range(self.grid_size[0]):
                for col in range(self.grid_size[1]):
                    cell_state = board_state['cells'][row][col]
                    btn = self.cell_buttons[row][col]
                    
                    if cell_state['is_revealed']:
                        btn.state = self.REVEALED
                        
                        if cell_state['is_mine']:
                            # Exploded mine
                            btn.config(
                                text='💣',
                                bg='#ff0000',
                                relief=tk.SUNKEN
                            )
                        elif cell_state['adjacent_mines'] > 0:
                            # Number
                            style = self.cell_images[str(cell_state['adjacent_mines'])]
                            btn.config(
                                text=str(cell_state['adjacent_mines']),
                                fg=style['fg'],
                                bg=style['bg'],
                                relief=tk.SUNKEN
                            )
                        else:
                            # Empty cell
                            btn.config(
                                text='',
                                bg='#e0e0e0',
                                relief=tk.SUNKEN
                            )
                    elif cell_state['is_flagged']:
                        btn.state = self.FLAGGED
                        btn.config(
                            text='🚩',
                            bg='#c0c0c0',
                            relief=tk.RAISED
                        )
    
    def _apply_windows7_style(self):
        """Apply Windows 7 style to the UI components."""
        # Try to use ttk styles for a more native look
        style = ttk.Style()
        
        # Use the system theme if available
        try:
            style.theme_use('vista')  # Windows 7 theme
        except tk.TclError:
            try:
                style.theme_use('winnative')  # Fallback to Windows native theme
            except tk.TclError:
                pass  # Use default theme if neither is available
        
        # Configure button style
        style.configure('TButton', padding=2)
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()


if __name__ == "__main__":
    # Create and run the game window for testing
    game_window = GameWindow()
    game_window.run()
