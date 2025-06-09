# Minesweeper Development Prompt Plan

This document outlines a series of prompts for building a Minesweeper game following the specifications. Each prompt builds incrementally on the previous one, following test-driven development principles.

## Project Structure Overview

Before diving into the prompts, here's the high-level structure of our Minesweeper implementation:

```
minesweeper/
├── assets/                # Images and resources
├── tests/                 # Test files
├── src/                   # Source code
│   ├── models/            # Game logic
│   ├── ui/                # User interface components
│   └── utils/             # Utility functions
├── main.py                # Entry point
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

## Development Plan

We'll develop the game in small, iterative chunks, starting with core game logic and gradually building up to a complete application.

---

## Prompt 1: Project Setup and Core Game Models

```
Create the initial project structure for a Minesweeper game based on the Windows 7 style.

1. Create a requirements.txt file with necessary dependencies (mainly Tkinter).
2. Set up a README.md with basic project information.
3. Create the core game model class that represents a Minesweeper cell with the following properties:
   - is_mine: Boolean indicating if the cell contains a mine
   - is_revealed: Boolean indicating if the cell has been revealed
   - is_flagged: Boolean indicating if the cell has been flagged
   - adjacent_mines: Integer representing the number of mines in adjacent cells
   - position: Tuple of (row, column) for the cell's position

4. Write unit tests for the cell class to verify:
   - Cell initialization with default values
   - Setting/getting cell properties
   - Basic cell behavior (toggling flags, revealing)

Follow test-driven development by writing tests first, then implementing the necessary code to make them pass.
```

---

## Prompt 2: Game Board Model

```
Now that we have the cell model, let's create the game board model:

1. Create a Board class that:
   - Initializes a 16x16 grid of Cell objects
   - Has a method to place 40 mines randomly on the board
   - Calculates adjacent mine counts for all cells
   - Handles revealing cells and implements the flood fill algorithm when revealing empty cells
   - Provides methods to check game state (won, lost, in progress)

2. Write comprehensive tests for the Board class to verify:
   - Board initialization with the correct dimensions
   - Mine placement logic (correct number, no duplicates)
   - Adjacent mine counting
   - Revealing cells behavior, including:
     - Revealing a mine ends the game
     - Revealing an empty cell reveals neighboring cells recursively
     - Revealing a numbered cell only reveals that cell
   - Game state checks (won when all non-mine cells are revealed, lost when a mine is revealed)

Ensure all tests pass before moving on to the next phase.
```

---

## Prompt 3: Game Controller

```
Let's create a GameController to manage game state and operations:

1. Create a GameController class that:
   - Manages the game board
   - Tracks game state (new, in progress, won, lost)
   - Implements a timer functionality to track game duration
   - Keeps track of the number of mines vs. flags placed
   - Handles player actions (revealing cells, toggling flags)
   - Provides a way to restart the game
   - Maintains a high score system

2. Write tests for the GameController to verify:
   - Game initialization
   - Game state transitions
   - Timer functionality
   - Flag counting
   - Action handling
   - Game restart capability

Ensure all components work together correctly before moving on to the user interface.
```

---

## Prompt 4: Basic UI Setup

```
Now let's start building the UI for our Minesweeper game using Tkinter:

1. Create a basic application window with:
   - A title bar showing "Minesweeper"
   - Fixed window size appropriate for a 16x16 grid
   - Windows 7 Minesweeper look-and-feel

2. Create placeholder frames for:
   - The top panel (for timer, mine counter, and restart button)
   - The game grid
   - A status bar (optional)

3. Write basic tests to verify the UI initialization and structure.

Focus on the foundation of the UI without implementing game logic integration yet.
```

---

## Prompt 5: UI Components

```
Let's implement the individual UI components for our Minesweeper game:

1. Create the top panel with:
   - A mine counter display (showing remaining mines)
   - A restart button with a smiley face icon
   - A timer display

2. Create the grid display component that:
   - Renders the 16x16 grid of cells
   - Shows different tile images based on cell state (unrevealed, revealed, flagged, mine, numbers)
   - Handles mouse clicks (left click to reveal, right click to flag)

3. Find or create appropriate assets for:
   - Cell states (revealed, unrevealed, flagged)
   - Number tiles (1-8)
   - Mine icon
   - Smiley face icons (normal, clicked, won, lost)

4. Write tests to verify:
   - UI component initialization
   - UI update mechanisms
   - User input handling

Ensure the UI components display correctly before integrating with the game logic.
```

---

## Prompt 6: UI-Logic Integration

```
Now let's connect the UI with the game logic:

1. Integrate the GameController with the UI:
   - Update the grid display when cells are revealed or flagged
   - Update the mine counter when flags are placed or removed
   - Update the timer every second during gameplay
   - Change the smiley face based on game state
   - Handle restart button clicks

2. Implement mouse event handling:
   - Left-click to reveal cells
   - Right-click to place/remove flags
   - Implement the middle-click to reveal adjacent cells (when appropriate)

3. Write integration tests to verify:
   - UI updates when game state changes
   - User interactions properly affect game state
   - Game status is properly reflected in UI elements

Ensure that the UI and game logic are working together seamlessly.
```

---

## Prompt 7: High Score System

```
Let's implement the high score system:

1. Create a HighScore class to represent a high score entry with:
   - Player name
   - Date achieved
   - Completion time

2. Implement functionality to:
   - Save high scores to a local file
   - Load high scores from a file
   - Sort and display the top scores

3. Create a high score dialog that:
   - Appears when a player wins with a qualifying score
   - Allows entering the player's name
   - Shows the current high score list

4. Write tests to verify:
   - High score saving and loading
   - Proper sorting of scores
   - Dialog functionality

Focus on making the high score system robust and user-friendly.
```

---

## Prompt 8: Error Handling and Polish

```
Let's implement comprehensive error handling and add final polish:

1. Add error handling for:
   - File operations (when saving/loading high scores)
   - User input validation
   - Exceptional game states

2. Add final polish:
   - Improve UI styling to match Windows 7 Minesweeper
   - Add proper spacing and alignment
   - Ensure consistent behavior across different actions
   - Add keyboard shortcuts (space for restart, etc.)

3. Write tests for error scenarios to ensure graceful handling.

Ensure the game is robust and provides a seamless user experience.
```

---

## Prompt 9: Package and Documentation

```
Let's finalize the project for distribution:

1. Create a comprehensive README with:
   - Project description
   - Installation instructions
   - How to play
   - Development information

2. Create a simple installer or setup script to make installation easy.

3. Document:
   - Code architecture
   - Testing approach
   - Any known limitations or future improvements

4. Perform final testing to ensure everything works together perfectly.

Ensure the project is well-documented and easy to install and run on Linux environments.
```

---

## Prompt 10: Finishing Touches and Final Testing

```
Let's apply finishing touches and perform final testing:

1. Conduct a thorough review of:
   - All game functionality
   - Visual appearance and consistency
   - Error handling in edge cases
   - Performance optimization

2. Perform user acceptance testing by playing through multiple games.

3. Address any remaining issues or inconsistencies.

4. Create a final release package.

Ensure the game is complete, polished, and ready for users to enjoy.
```

---

## Testing Strategy

Throughout the development process, we follow these testing principles:

1. **Unit Testing**: Test individual components in isolation
2. **Integration Testing**: Test how components work together
3. **Functional Testing**: Test complete game functionality
4. **User Interface Testing**: Test UI appearance and interactions

Each prompt builds on the previous ones, ensuring that no code is orphaned and all pieces fit together logically. The incremental approach allows for continuous testing and refinement at each step.
