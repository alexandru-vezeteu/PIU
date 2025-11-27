"""
Command for adding text items.

Stores the text graphics item and can add/remove it from the scene.
"""

from PyQt5.QtWidgets import QGraphicsItem
from src.core.command import ICommand


class TextCommand(ICommand):
    """Command for text operations."""
    
    def __init__(self, text_item: QGraphicsItem):
        """
        Initialize text command.
        
        Args:
            text_item: The text graphics item to add to scene
        """
        self.text_item = text_item
    
    def execute(self, scene):
        """Add the text item to the scene."""
        scene.addItem(self.text_item)
    
    def undo(self, scene):
        """Remove the text item from the scene."""
        scene.removeItem(self.text_item)
    
    def get_name(self) -> str:
        """Get command name."""
        return "Add Text"
