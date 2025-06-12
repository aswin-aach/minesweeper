"""High score dialog for displaying and entering high scores."""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import Callable, Optional

from src.models.high_score import HighScoreManager, HighScoreEntry

class HighScoreDialog:
    """Dialog for displaying high scores and entering new ones."""
    
    def __init__(self, parent: tk.Tk, high_score_manager: HighScoreManager):
        self.parent = parent
        self.high_score_manager = high_score_manager
        self.dialog: Optional[tk.Toplevel] = None
        self.name_var: Optional[tk.StringVar] = None
        self.on_submit_callback: Optional[Callable] = None
        
    def show_high_scores(self):
        """Display the high scores dialog."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("High Scores")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        window_width = 400
        window_height = 300
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create and configure the treeview
        columns = ("Rank", "Player", "Time", "Date")
        tree = ttk.Treeview(self.dialog, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Add high scores to the treeview
        for i, score in enumerate(self.high_score_manager.get_scores(), 1):
            date = datetime.fromisoformat(score.date_achieved).strftime("%Y-%m-%d")
            tree.insert("", "end", values=(
                f"#{i}",
                score.player_name,
                f"{score.completion_time:.1f}s",
                date
            ))
        
        # Pack widgets
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        close_btn = ttk.Button(self.dialog, text="Close", command=self.dialog.destroy)
        close_btn.pack(pady=10)
        
    def prompt_for_name(self, completion_time: float, callback: Callable[[str], None]):
        """Show dialog to enter name for new high score."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("New High Score!")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        window_width = 300
        window_height = 150
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Congratulations message
        msg = f"Congratulations! You completed the game in {completion_time:.1f} seconds!"
        label = ttk.Label(self.dialog, text=msg, wraplength=250)
        label.pack(pady=10)
        
        # Name entry
        self.name_var = tk.StringVar()
        name_frame = ttk.Frame(self.dialog)
        name_frame.pack(pady=10)
        
        name_label = ttk.Label(name_frame, text="Enter your name:")
        name_label.pack(side="left", padx=5)
        
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var)
        name_entry.pack(side="left", padx=5)
        name_entry.focus()
        
        # Submit button
        def on_submit():
            name = self.name_var.get().strip()
            if name:
                self.dialog.destroy()
                callback(name)
        
        submit_btn = ttk.Button(self.dialog, text="Submit", command=on_submit)
        submit_btn.pack(pady=10)
        
        # Bind Enter key to submit
        self.dialog.bind('<Return>', lambda e: on_submit())
