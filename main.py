#!/usr/bin/env python3
"""
Minesweeper Game - Main Entry Point
A classic Minesweeper clone based on the Windows 7 style.
"""

import tkinter as tk
from src.models.board import Board
from src.models.cell import Cell
from src.controllers.game_controller import GameController
from src.ui.game_window import GameWindow


def main():
    # Create the root window
    root = tk.Tk()
    
    # Create a game controller
    game_controller = GameController()
    
    # Create the game window with the controller
    game_window = GameWindow(root, controller=game_controller)
    
    # Set up periodic UI updates from controller
    def update_ui_from_controller():
        # Get current game state from controller
        board = game_controller.board
        
        # Create cell data for the board state
        cells = []
        for row in range(board.rows):
            cell_row = []
            for col in range(board.cols):
                cell = board.get_cell(row, col)
                cell_data = {
                    'is_revealed': cell.is_revealed,
                    'is_flagged': cell.is_flagged,
                    'is_mine': cell.is_mine,
                    'adjacent_mines': cell.adjacent_mines
                }
                cell_row.append(cell_data)
            cells.append(cell_row)
        
        board_state = {
            'mines_remaining': game_controller.get_remaining_mines(),
            'elapsed_time': game_controller.get_elapsed_time(),
            'game_state': game_controller.game_state,
            'cells': cells
        }
        
        # Update UI with current state
        game_window.update_from_controller(board_state)
        
        # Schedule the next update
        root.after(100, update_ui_from_controller)
    
    # Start the periodic updates
    update_ui_from_controller()
    
    # Start the main event loop
    root.mainloop()
    

def console_demo():
    """Run a console-based demo of the game controller."""
    # Create a new game controller
    game = GameController()
    
    print("=== Minesweeper Game Demo ===\n")
    
    # Game starts in 'new' state
    print(f"Game State: {game.game_state}")
    print(f"Elapsed Time: {game.get_elapsed_time()} seconds")
    print(f"Remaining Mines: {game.get_remaining_mines()}")
    
    # Start the game (places mines)
    print("\nStarting game...")
    game.start_game()
    print(f"Game State: {game.game_state}")
    
    # Print the initial board (mines are hidden)
    print("\nInitial Board:")
    print_board(game.board)
    
    # Reveal a cell
    print("\nRevealing cell at (5, 5):")
    game.reveal_cell(5, 5)
    print_board(game.board)
    print(f"Game State: {game.game_state}")
    print(f"Elapsed Time: {game.get_elapsed_time()} seconds")
    
    # Flag a cell
    print("\nFlagging cell at (10, 10):")
    game.toggle_flag(10, 10)
    print_board(game.board)
    print(f"Remaining Mines: {game.get_remaining_mines()}")
    
    # Demonstrate restarting the game
    print("\nRestarting game...")
    game.restart_game()
    print(f"Game State: {game.game_state}")
    print(f"Elapsed Time: {game.get_elapsed_time()} seconds")
    print(f"Remaining Mines: {game.get_remaining_mines()}")
    
    # Demonstrate high score functionality
    print("\nSimulating a won game and adding a high score...")
    game.start_game()
    game.game_state = 'won'  # Force a win for demonstration
    game.elapsed_time = 120  # Set a time of 120 seconds
    game.add_high_score("Player1")
    
    print("\nHigh Scores:")
    for i, score in enumerate(game.get_high_scores()):
        print(f"{i+1}. {score['name']}: {score['time']} seconds ({score['date']})")

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    print("   ", end="")
    for col in range(board.cols):
        print(f"{col:2}", end=" ")
    print()
    
    # Print horizontal separator
    print("   " + "-" * (board.cols * 3))
    
    for row in range(board.rows):
        # Print row header
        print(f"{row:2} |", end=" ")
        
        for col in range(board.cols):
            cell = board.grid[row][col]
            if cell.is_flagged:
                print("F ", end=" ")
            elif not cell.is_revealed:
                print("# ", end=" ")
            elif cell.is_mine:
                print("* ", end=" ")
            elif cell.adjacent_mines == 0:
                print(". ", end=" ")
            else:
                print(f"{cell.adjacent_mines} ", end=" ")
        print()

if __name__ == "__main__":
    # Run the GUI version
    main()
    
    # Uncomment to run the console demo instead
    # console_demo()
