class Cell:
    """
    Represents a single cell in the Minesweeper game grid.
    
    Attributes:
        position (tuple): The (row, column) position of the cell in the grid.
        is_mine (bool): Whether the cell contains a mine.
        is_revealed (bool): Whether the cell has been revealed by the player.
        is_flagged (bool): Whether the cell has been flagged by the player.
        adjacent_mines (int): The number of mines in adjacent cells.
    """
    
    def __init__(self, row, col, is_mine=False):
        """
        Initialize a new Cell.
        
        Args:
            row (int): The row position of the cell.
            col (int): The column position of the cell.
            is_mine (bool, optional): Whether the cell contains a mine. Defaults to False.
        """
        self.position = (row, col)
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
    
    def toggle_flag(self):
        """
        Toggle the flag status of the cell.
        
        Returns:
            bool: True if the flag was toggled, False otherwise.
        """
        # Cannot flag a revealed cell
        if self.is_revealed:
            return False
        
        self.is_flagged = not self.is_flagged
        return True
    
    def reveal(self):
        """
        Reveal the cell.
        
        Returns:
            bool: True if the cell contains a mine, False otherwise.
        """
        # Cannot reveal a flagged cell
        if self.is_flagged:
            return False
        
        self.is_revealed = True
        return self.is_mine
    
    def __str__(self):
        """
        Return a string representation of the cell.
        
        Returns:
            str: A string describing the cell.
        """
        mine_status = "Mine" if self.is_mine else "Empty"
        revealed_status = "Revealed" if self.is_revealed else "Hidden"
        flagged_status = "Flagged" if self.is_flagged else "Unflagged"
        
        return f"Cell at {self.position}: {mine_status}, {revealed_status}, {flagged_status}, Adjacent mines: {self.adjacent_mines}"
    
    def __repr__(self):
        """
        Return a string representation for debugging.
        
        Returns:
            str: A string representation of the cell.
        """
        return self.__str__()
