"""
Command for adding shapes (rectangle, circle, line).

Stores the shape graphics item and can add/remove it from the scene.
"""

from PyQt5.QtWidgets import QGraphicsItem
from src.core.command import ICommand


class ShapeCommand(ICommand):
    """Command for shape drawing operations."""
    
    def __init__(self, shape_item: QGraphicsItem, shape_type: str = "Shape"):
        """
        Initialize shape command.
        
        Args:
            shape_item: The shape graphics item to add to scene
            shape_type: Type of shape (Rectangle, Circle, Line)
        """
        self.shape_item = shape_item
        self.shape_type = shape_type
    
    def execute(self, scene):
        """Add the shape to the scene."""
        scene.addItem(self.shape_item)
    
    def undo(self, scene):
        """Remove the shape from the scene."""
        scene.removeItem(self.shape_item)
    
    def get_name(self) -> str:
        """Get command name."""
        return f"Add {self.shape_type}"
