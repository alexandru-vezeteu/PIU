"""
Command for pixel-based drawing operations.

Stores before/after QImage snapshots for undo/redo functionality.
"""

from PyQt5.QtGui import QImage
from src.core.command import ICommand


class PixelDrawCommand(ICommand):
    """Command for pixel-based brush/eraser drawing operations."""
    
    def __init__(self, before_image: QImage, after_image: QImage, name: str = "Draw"):
        """
        Initialize pixel draw command.
        
        Args:
            before_image: Canvas state before drawing
            after_image: Canvas state after drawing
            name: Display name for the command
        """
        self.before_image = before_image.copy()
        self.after_image = after_image.copy()
        self.name = name
    
    def execute(self, scene):
        """Apply the after image to the canvas."""
        from PyQt5.QtGui import QPixmap
        items = scene.items()
        
        for item in items:
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                item.setPixmap(QPixmap.fromImage(self.after_image))
                break
    
    def undo(self, scene):
        """Restore the before image to the canvas."""
        from PyQt5.QtGui import QPixmap
        items = scene.items()
        
        for item in items:
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                item.setPixmap(QPixmap.fromImage(self.before_image))
                break
    
    def get_name(self) -> str:
        """Get command name."""
        return self.name
