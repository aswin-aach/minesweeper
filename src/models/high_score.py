"""High score management for Minesweeper."""
print('Loading high_score.py...')
print('Current directory:', __file__)
from dataclasses import dataclass
from datetime import datetime
import json
import os
import traceback
print('Testing os.getcwd():', os.getcwd())
from pathlib import Path
from typing import List
print('os module:', os)

@dataclass
class HighScoreEntry:
    """Represents a single high score entry."""
    player_name: str
    completion_time: float  # in seconds
    date_achieved: str
    
    @classmethod
    def create(cls, player_name: str, completion_time: float) -> 'HighScoreEntry':
        """Create a new high score entry with current timestamp."""
        return cls(
            player_name=player_name,
            completion_time=completion_time,
            date_achieved=datetime.now().isoformat()
        )
    
    def to_dict(self) -> dict:
        """Convert entry to dictionary for serialization."""
        return {
            'player_name': self.player_name,
            'completion_time': self.completion_time,
            'date_achieved': self.date_achieved
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'HighScoreEntry':
        """Create entry from dictionary."""
        return cls(**data)

class HighScoreManager:
    """Manages high score operations."""
    try:
        # Define scores directory at class level
        print('Defining SCORES_DIR...')
        SCORES_DIR = Path(os.path.expanduser('~')) / '.minesweeper'
        print('SCORES_DIR defined successfully:', SCORES_DIR)
    except Exception as e:
        print('Error defining SCORES_DIR:')
        traceback.print_exc()
        raise
    
    def __init__(self, max_scores: int = 10):
        try:
            print('Initializing HighScoreManager')
            self.max_scores = max_scores
            self.scores: List[HighScoreEntry] = []
            print('Creating scores file path...')
            # Use class-level constant
            self.scores_file = self.SCORES_DIR / 'highscores.json'
            print('Scores file path:', self.scores_file)
            self.scores_file.parent.mkdir(parents=True, exist_ok=True)
            self.load_scores()
        except Exception as e:
            print('Error in HighScoreManager initialization:')
            traceback.print_exc()
            raise
    
    def add_score(self, player_name: str, completion_time: float) -> bool:
        """
        Add a new high score. Returns True if score qualifies for high score list.
        """
        # Load latest scores before adding new one
        self.load_scores()
        
        new_score = HighScoreEntry.create(player_name, completion_time)
        
        # Always add score if we haven't reached max_scores
        if len(self.scores) < self.max_scores:
            self.scores.append(new_score)
            self._sort_scores()
            self.save_scores()
            return True
        
        # Otherwise, only add if it's better than the worst score
        if completion_time < self.scores[-1].completion_time:
            self.scores = self.scores[:-1]  # Remove the worst score
            self.scores.append(new_score)
            self._sort_scores()
            self.save_scores()
            return True
            
        return False
    
    def _sort_scores(self):
        """Sort scores by completion time (ascending)."""
        self.scores.sort(key=lambda x: x.completion_time)
    
    def load_scores(self):
        """Load scores from file."""
        self.scores = []
        try:
            if self.scores_file.exists():
                with open(self.scores_file, 'r') as f:
                    data = json.load(f)
                    for entry in data:
                        score = HighScoreEntry.from_dict(entry)
                        self.scores.append(score)
                    self._sort_scores()
                    # Trim to max_scores
                    if len(self.scores) > self.max_scores:
                        self.scores = self.scores[:self.max_scores]
        except Exception as e:
            print(f"Error loading high scores: {e}")
            print(traceback.format_exc())
    
    def save_scores(self):
        """Save high scores to file."""
        try:
            # Create directory if it doesn't exist
            self.SCORES_DIR.mkdir(parents=True, exist_ok=True)
            
            # Save scores to file
            with open(self.scores_file, 'w') as f:
                json.dump([score.to_dict() for score in self.scores], f)
        except Exception as e:
            print(f"Error saving high scores: {e}")
            traceback.print_exc()
            
    def clear_scores(self):
        """Clear all high scores."""
        self.scores = []
        self.save_scores()
    
    def get_scores(self) -> List[HighScoreEntry]:
        """Get all high scores."""
        return self.scores.copy()

    def qualifies_for_high_score(self, completion_time: float) -> bool:
        """Check if a given completion time qualifies for the high score list."""
        # Load latest scores before checking
        self.load_scores()
        
        if len(self.scores) < self.max_scores:
            return True
        # Get the worst score (highest completion time)
        worst_score = max(self.scores, key=lambda x: x.completion_time)
        return completion_time < worst_score.completion_time
