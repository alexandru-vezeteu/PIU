from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor


class CanvasView(QGraphicsView):
    """Custom QGraphicsView that forwards mouse events to active tool"""

    def __init__(self, document, tool_manager):
        super().__init__(document.scene)
        self.document = document
        self.tool_manager = tool_manager
        
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        
        self.setBackgroundBrush(QBrush(QColor(255, 255, 255)))
        
        self.setSceneRect(document.scene.sceneRect())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def mousePressEvent(self, event):
        """Forward mouse press to active tool"""
        current_tool = self.tool_manager.get_current_tool()
        if current_tool:
            current_tool.mouse_press_event(event, self.document.scene, self)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Forward mouse move to active tool"""
        current_tool = self.tool_manager.get_current_tool()
        if current_tool:
            current_tool.mouse_move_event(event, self.document.scene, self)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Forward mouse release to active tool and execute command if returned"""
        current_tool = self.tool_manager.get_current_tool()
        if current_tool:
            command = current_tool.mouse_release_event(event, self.document.scene, self)
            if command:
                self.document.execute_command(command)
                parent = self.window()
                if hasattr(parent, 'update_undo_redo_states'):
                    parent.update_undo_redo_states()
        super().mouseReleaseEvent(event)
    
    def wheelEvent(self, event):
        """Handle mouse wheel for zooming."""
        if event.modifiers() == Qt.ControlModifier:
            zoom_in_factor = 1.15
            zoom_out_factor = 1 / zoom_in_factor
            
            old_pos = self.mapToScene(event.pos())
            
            if event.angleDelta().y() > 0:
                zoom_factor = zoom_in_factor
            else:
                zoom_factor = zoom_out_factor
            
            self.scale(zoom_factor, zoom_factor)
            
            new_pos = self.mapToScene(event.pos())
            delta = new_pos - old_pos
            self.translate(delta.x(), delta.y())
            
            event.accept()
        else:
            super().wheelEvent(event)
