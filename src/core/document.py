"""
Document class that wraps QGraphicsScene and manages command history.

This is the central state manager for the paint application.
"""

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QImage, QPainter, QPixmap, QColor
from src.core.command_history import CommandHistory
from src.core.command import ICommand


class Document:
    """
    Document manages the canvas state and command history.
    
    All operations on the canvas should go through execute_command()
    to ensure they can be undone/redone.
    """
    
    def __init__(self, width=1920, height=1080):
        """
        Initialize document with scene and command history.
        
        Args:
            width: Canvas width in pixels (default: 1920)
            height: Canvas height in pixels (default: 1080)
        """
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, width, height)
        self.history = CommandHistory(max_undo=20)
        self.width = width
        self.height = height
        self.stroke_count = 0
        self.flatten_threshold = 50  
        self.background_pixmap_item = None
        
        self.canvas_image = QImage(int(width), int(height), QImage.Format_ARGB32)
        self.canvas_image.fill(0x00000000)  # Transparent background
        
        checkerboard = self._create_checkerboard(int(width), int(height))
        self.checkerboard_item = QGraphicsPixmapItem(checkerboard)
        self.checkerboard_item.setData(0, 'checkerboard')
        self.checkerboard_item.setZValue(-1)  # Behind canvas
        self.scene.addItem(self.checkerboard_item)
        
        self.canvas_pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(self.canvas_image))
        self.canvas_pixmap_item.setData(0, 'canvas')  # Tag for identification
        self.scene.addItem(self.canvas_pixmap_item)
    
    def _create_checkerboard(self, width, height, square_size=16):
        """Create a checkerboard pattern to show transparency."""
        checkerboard = QImage(width, height, QImage.Format_RGB32)
        painter = QPainter(checkerboard)
        
        light_gray = QColor(200, 200, 200)
        dark_gray = QColor(150, 150, 150)
        
        for y in range(0, height, square_size):
            for x in range(0, width, square_size):
                if ((x // square_size) + (y // square_size)) % 2 == 0:
                    painter.fillRect(x, y, square_size, square_size, light_gray)
                else:
                    painter.fillRect(x, y, square_size, square_size, dark_gray)
        
        painter.end()
        return QPixmap.fromImage(checkerboard)
    
    def get_canvas_image(self):
        """Get the current canvas image for pixel-based drawing."""
        return self.canvas_pixmap_item.pixmap().toImage()
    
    def execute_command(self, command: ICommand):
        """
        Execute a command and add to history.
        
        Args:
            command: The command to execute
        """
        self.history.execute(command, self.scene)
        
        from src.commands.pixel_draw_command import PixelDrawCommand
        if isinstance(command, PixelDrawCommand):
            self.stroke_count += 1
            if self.stroke_count >= self.flatten_threshold:
                self.flatten_layers()
                self.stroke_count = 0
    
    def flatten_layers(self):
        """Flatten all scene items into a single background image for performance."""
        from PyQt5.QtGui import QImage, QPainter, QPixmap
        from PyQt5.QtWidgets import QGraphicsPixmapItem
        
        canvas_rect = QRectF(0, 0, self.width, self.height)
        image = QImage(int(self.width), int(self.height), QImage.Format_ARGB32)
        image.fill(0x00000000)
        
        items_to_hide = []
        for item in self.scene.items():
            if item.data(0) == 'checkerboard' or item.data(0) == 'selection':
                if item.isVisible():
                    items_to_hide.append(item)
                    item.setVisible(False)
            
        painter = QPainter(image)
        self.scene.render(painter, QRectF(), canvas_rect)
        painter.end()
        
            item.setVisible(True)
        
        self.scene.clear()
        
        checkerboard = self._create_checkerboard(int(self.width), int(self.height))
        self.checkerboard_item = QGraphicsPixmapItem(checkerboard)
        self.checkerboard_item.setData(0, 'checkerboard')
        self.checkerboard_item.setZValue(-1)
        self.scene.addItem(self.checkerboard_item)
        
        self.canvas_image = image
        self.canvas_pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(image))
        self.canvas_pixmap_item.setData(0, 'canvas')
        self.scene.addItem(self.canvas_pixmap_item)
        
        self.history.clear()
        
        print(f"[Performance] Flattened {self.flatten_threshold} strokes into background")
    
    def undo(self) -> bool:
        """
        Undo the last command.
        
        Returns:
            bool: True if undo was performed
        """
        return self.history.undo(self.scene)
    
    def redo(self) -> bool:
        """
        Redo the last undone command.
        
        Returns:
            bool: True if redo was performed
        """
        return self.history.redo(self.scene)
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self.history.can_undo()
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self.history.can_redo()
    
    def get_undo_name(self) -> str:
        """Get name of command that would be undone."""
        return self.history.get_undo_name()
    
    def get_redo_name(self) -> str:
        """Get name of command that would be redone."""
        return self.history.get_redo_name()
    
    def clear_history(self):
        """Clear all undo/redo history."""
        self.history.clear()
