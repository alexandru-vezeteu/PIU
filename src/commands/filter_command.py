"""
Command for applying filters to the canvas.

Stores a snapshot of the scene before applying the filter for undo.
"""

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import QRectF
from src.core.command import ICommand


class FilterCommand(ICommand):
    """Command for filter operations."""
    
    def __init__(self, scene, filter_func, filter_name="Filter", canvas_rect=None):
        """
        Initialize filter command.
        
        Args:
            scene: QGraphicsScene to operate on
            filter_func: Function that takes QImage and returns filtered QImage
            filter_name: Display name for the filter
            canvas_rect: Optional QRectF for actual canvas area (defaults to scene rect)
        """
        self.filter_name = filter_name
        self.filter_func = filter_func
        
        self.canvas_item = None
        for item in scene.items():
            if isinstance(item, QGraphicsPixmapItem) and item.data(0) == 'canvas':
                self.canvas_item = item
                break
        
        if not self.canvas_item:
            raise ValueError("Canvas item not found in scene")
        
        self.before_image = self.canvas_item.pixmap().toImage()
        
        self.after_image = filter_func(self.before_image.copy())
    
    def _apply_image_to_canvas(self, scene, image):
        """Replace only the canvas pixmap with the given image."""
        canvas_item = None
        for item in scene.items():
            if isinstance(item, QGraphicsPixmapItem) and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if canvas_item:
            canvas_item.setPixmap(QPixmap.fromImage(image))
    
    def execute(self, scene):
        """Apply the filter to the canvas."""
        self._apply_image_to_canvas(scene, self.after_image)
    
    def undo(self, scene):
        """Restore the canvas to before the filter was applied."""
        self._apply_image_to_canvas(scene, self.before_image)
    
    def get_name(self) -> str:
        """Get command name."""
        return f"{self.filter_name} Filter"
