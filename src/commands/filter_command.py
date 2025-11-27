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
    
    def __init__(self, scene, filter_func, filter_name="Filter"):
        """
        Initialize filter command.
        
        Args:
            scene: QGraphicsScene to operate on
            filter_func: Function that takes QImage and returns filtered QImage
            filter_name: Display name for the filter
        """
        self.filter_name = filter_name
        self.filter_func = filter_func
        
        self.before_image = self._capture_scene(scene)
        
        self.after_image = filter_func(self.before_image.copy())
        
    def _capture_scene(self, scene):
        """Capture the current scene as a QImage."""
        rect = scene.sceneRect()
        image = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB32)
        image.fill(0xFFFFFFFF) 
        
        painter = QPainter(image)
        scene.render(painter)
        painter.end()
        
        return image
    
    def _apply_image_to_scene(self, scene, image):
        """Replace scene contents with the given image."""
        scene.clear()
        
        pixmap = QPixmap.fromImage(image)
        scene.addPixmap(pixmap)
    
    def execute(self, scene):
        """Apply the filter to the scene."""
        self._apply_image_to_scene(scene, self.after_image)
    
    def undo(self, scene):
        """Restore the scene to before the filter was applied."""
        self._apply_image_to_scene(scene, self.before_image)
    
    def get_name(self) -> str:
        """Get command name."""
        return f"{self.filter_name} Filter"
