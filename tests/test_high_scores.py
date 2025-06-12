"""Tests for the high score system."""
import unittest
from datetime import datetime
import tempfile
from pathlib import Path
import json

from src.models.high_score import HighScoreEntry, HighScoreManager

class TestHighScores(unittest.TestCase):
    """Test cases for high score functionality."""
    
    def setUp(self):
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.scores_path = Path(self.temp_dir) / 'test_highscores.json'
        
        # Create a new manager instance for each test
        self.manager = HighScoreManager(max_scores=3)
        # Override the scores_file path after creation
        self.manager.scores_file = self.scores_path
        # Ensure we start with a clean state
        if self.scores_path.exists():
            self.scores_path.unlink()
    
    def test_high_score_entry_creation(self):
        """Test creation of high score entries."""
        entry = HighScoreEntry.create("TestPlayer", 100.5)
        self.assertEqual(entry.player_name, "TestPlayer")
        self.assertEqual(entry.completion_time, 100.5)
        self.assertTrue(isinstance(entry.date_achieved, str))
    
    def test_high_score_serialization(self):
        """Test serialization and deserialization of high scores."""
        original = HighScoreEntry.create("TestPlayer", 100.5)
        data = original.to_dict()
        restored = HighScoreEntry.from_dict(data)
        
        self.assertEqual(original.player_name, restored.player_name)
        self.assertEqual(original.completion_time, restored.completion_time)
        self.assertEqual(original.date_achieved, restored.date_achieved)
    
    def test_score_sorting(self):
        """Test that scores are properly sorted."""
        self.manager.add_score("Player1", 100.0)
        self.manager.add_score("Player2", 50.0)
        self.manager.add_score("Player3", 75.0)
        
        scores = self.manager.get_scores()
        self.assertEqual(len(scores), 3)
        self.assertEqual(scores[0].completion_time, 50.0)
        self.assertEqual(scores[1].completion_time, 75.0)
        self.assertEqual(scores[2].completion_time, 100.0)
    
    def test_max_scores_limit(self):
        """Test that max scores limit is enforced."""
        self.manager.add_score("Player1", 100.0)
        self.manager.add_score("Player2", 50.0)
        self.manager.add_score("Player3", 75.0)
        self.manager.add_score("Player4", 60.0)  # Should replace 100.0
        
        scores = self.manager.get_scores()
        self.assertEqual(len(scores), 3)
        self.assertEqual(scores[0].completion_time, 50.0)
        self.assertEqual(scores[2].completion_time, 75.0)
    
    def test_score_persistence(self):
        """Test saving and loading scores."""
        self.manager.add_score("Player1", 100.0)
        self.manager.add_score("Player2", 50.0)

        # Create a new manager instance to test loading
        new_manager = HighScoreManager(max_scores=3)
        new_manager.scores_file = self.scores_path
        new_manager.load_scores()
        scores = new_manager.get_scores()
        
        self.assertEqual(len(scores), 2)
        self.assertEqual(scores[0].completion_time, 50.0)
        self.assertEqual(scores[1].completion_time, 100.0)
    
    def test_score_qualification(self):
        """Test score qualification logic."""
        self.manager.add_score("Player1", 100.0)
        self.manager.add_score("Player2", 50.0)
        self.manager.add_score("Player3", 75.0)
        
        # Test qualification when list is full
        self.assertTrue(self.manager.qualifies_for_high_score(60.0))
        self.assertFalse(self.manager.qualifies_for_high_score(120.0))
        
        # Test qualification when list isn't full
        new_manager = HighScoreManager(max_scores=5)
        self.assertTrue(new_manager.qualifies_for_high_score(200.0))
