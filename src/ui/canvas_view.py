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
        
        self.setCacheMode(QGraphicsView.CacheNone)
        
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        
        canvas_rect = document.scene.sceneRect()
        margin = max(canvas_rect.width(), canvas_rect.height()) * 10
        self.setSceneRect(
            canvas_rect.x() - margin,
            canvas_rect.y() - margin,
            canvas_rect.width() + 2 * margin,
            canvas_rect.height() + 2 * margin
        )
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.current_zoom = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 10.0
        
        self.is_panning = False
        self.last_pan_pos = None
    
    def reset_zoom_tracking(self):
        """Reset zoom tracking to 1.0 - call this after resetTransform or fitInView."""
        self.current_zoom = 1.0

    def mousePressEvent(self, event):
        """Forward mouse press to active tool or handle panning"""
        if event.modifiers() == Qt.ControlModifier and event.button() == Qt.LeftButton:
            self.is_panning = True
            self.last_pan_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        
        current_tool = self.tool_manager.get_current_tool()
        if current_tool:
            current_tool.mouse_press_event(event, self.document.scene, self)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Forward mouse move to active tool or handle panning"""
        if self.is_panning and self.last_pan_pos is not None:
            delta = event.pos() - self.last_pan_pos
            self.last_pan_pos = event.pos()
            
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )
            event.accept()
            return
        
        current_tool = self.tool_manager.get_current_tool()
        if current_tool:
            current_tool.mouse_move_event(event, self.document.scene, self)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Forward mouse release to active tool and execute command if returned"""
        if self.is_panning and event.button() == Qt.LeftButton:
            self.is_panning = False
            self.last_pan_pos = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        
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
            
            new_zoom = self.current_zoom * zoom_factor
            if new_zoom < self.min_zoom or new_zoom > self.max_zoom:
                event.accept()
                return
            
            self.current_zoom = new_zoom
            self.scale(zoom_factor, zoom_factor)
            
            new_pos = self.mapToScene(event.pos())
            delta = new_pos - old_pos
            self.translate(delta.x(), delta.y())
            
            event.accept()
        else:
            super().wheelEvent(event)
