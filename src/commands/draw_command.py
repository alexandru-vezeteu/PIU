"""
Command for drawing operations (brush strokes, eraser).

Stores the graphics item and can add/remove it from the scene.
"""

from PyQt5.QtWidgets import QGraphicsItem
from src.core.command import ICommand


class DrawCommand(ICommand):
    """Command for brush/eraser drawing operations."""
    
    def __init__(self, graphics_item: QGraphicsItem, name: str = "Draw"):
        """
        Initialize draw command.
        
        Args:
            graphics_item: The graphics item to add to scene
            name: Display name for the command
        """
        self.graphics_item = graphics_item
        self.name = name
    
    def execute(self, scene):
        """Add the graphics item to the scene."""
        scene.addItem(self.graphics_item)
    
    def undo(self, scene):
        """Remove the graphics item from the scene."""
        scene.removeItem(self.graphics_item)
    
    def get_name(self) -> str:
        """Get command name."""
        return self.name
