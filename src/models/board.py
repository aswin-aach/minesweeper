import random
from src.models.cell import Cell


class Board:
    """
    Represents the Minesweeper game board.
    
    Attributes:
        grid (list): A 2D list of Cell objects representing the game grid.
        game_state (str): The current state of the game ('new', 'in_progress', 'won', 'lost').
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
    """
    
    def __init__(self, rows=16, cols=16):
        """
        Initialize a new game board.
        
        Args:
            rows (int, optional): The number of rows in the grid. Defaults to 16.
            cols (int, optional): The number of columns in the grid. Defaults to 16.
        """
        self.rows = rows
        self.cols = cols
        self.game_state = 'new'
        
        # Initialize the grid with empty cells
        self.grid = []
        for row in range(rows):
            row_cells = []
            for col in range(cols):
                row_cells.append(Cell(row, col))
            self.grid.append(row_cells)
    
    def place_mines(self, num_mines):
        """
        Randomly place mines on the board.
        
        Args:
            num_mines (int): The number of mines to place.
        """
        # Create a list of all possible positions
        all_positions = [(row, col) for row in range(self.rows) for col in range(self.cols)]
        
        # Randomly select positions for mines
        mine_positions = random.sample(all_positions, num_mines)
        
        # Place mines at the selected positions
        for row, col in mine_positions:
            self.grid[row][col].is_mine = True
        
        # Calculate adjacent mine counts
        self.calculate_adjacent_mines()
        
        # Update game state
        self.game_state = 'in_progress'
    
    def calculate_adjacent_mines(self):
        """Calculate the number of adjacent mines for each cell."""
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.grid[row][col].is_mine:
                    # Get all neighboring cells
                    neighbors = self.get_neighbors(row, col)
                    
                    # Count mines in neighboring cells
                    mine_count = sum(1 for neighbor in neighbors if neighbor.is_mine)
                    
                    # Set the adjacent mine count
                    self.grid[row][col].adjacent_mines = mine_count
    
    def get_cell(self, row, col):
        """
        Get the cell at the specified position.
        
        Args:
            row (int): The row index.
            col (int): The column index.
            
        Returns:
            Cell or None: The cell at the specified position, or None if out of bounds.
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None
    
    def get_neighbors(self, row, col):
        """
        Get all neighboring cells for a given position.
        
        Args:
            row (int): The row index.
            col (int): The column index.
            
        Returns:
            list: A list of neighboring Cell objects.
        """
        neighbors = []
        
        # Check all 8 possible neighboring positions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Skip the cell itself
                if dr == 0 and dc == 0:
                    continue
                
                # Calculate neighbor position
                neighbor_row = row + dr
                neighbor_col = col + dc
                
                # Get the neighbor cell if it's within bounds
                neighbor = self.get_cell(neighbor_row, neighbor_col)
                if neighbor:
                    neighbors.append(neighbor)
        
        return neighbors
    
    def reveal_cell(self, row, col):
        """
        Reveal a cell at the specified position.
        
        Args:
            row (int): The row index.
            col (int): The column index.
            
        Returns:
            bool: True if the game state changed, False otherwise.
        """
        cell = self.get_cell(row, col)
        
        # Check if the cell is valid and not already revealed or flagged
        if not cell or cell.is_revealed or cell.is_flagged:
            return False
        
        # Reveal the cell
        is_mine = cell.reveal()
        
        # If it's a mine, the game is lost
        if is_mine:
            self.game_state = 'lost'
            return True
        
        # If it has no adjacent mines, reveal neighboring cells recursively
        if cell.adjacent_mines == 0:
            for neighbor in self.get_neighbors(row, col):
                if not neighbor.is_revealed and not neighbor.is_flagged:
                    self.reveal_cell(neighbor.position[0], neighbor.position[1])
        
        # Check if the game is won
        self._check_win_condition()
        
        return True
    
    def toggle_flag(self, row, col):
        """
        Toggle the flag on a cell.
        
        Args:
            row (int): The row index.
            col (int): The column index.
            
        Returns:
            bool: True if the flag was toggled, False otherwise.
        """
        cell = self.get_cell(row, col)
        
        # Check if the cell is valid and not already revealed
        if not cell or cell.is_revealed:
            return False
        
        # Toggle the flag
        return cell.toggle_flag()
    
    def _check_win_condition(self):
        """
        Check if the game has been won.
        
        The game is won when all non-mine cells are revealed.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                # If there's a non-mine cell that's not revealed, the game is not won yet
                if not cell.is_mine and not cell.is_revealed:
                    return
        
        # All non-mine cells are revealed, so the game is won
        self.game_state = 'won'
    
    def __str__(self):
        """
        Return a string representation of the board.
        
        Returns:
            str: A string representation of the board.
        """
        result = []
        for row in self.grid:
            row_str = []
            for cell in row:
                if cell.is_revealed:
                    if cell.is_mine:
                        row_str.append('*')
                    elif cell.adjacent_mines > 0:
                        row_str.append(str(cell.adjacent_mines))
                    else:
                        row_str.append(' ')
                elif cell.is_flagged:
                    row_str.append('F')
                else:
                    row_str.append('.')
            result.append(' '.join(row_str))
        
        return '\n'.join(result)
