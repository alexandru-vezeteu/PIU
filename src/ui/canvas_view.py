from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor


class CanvasView(QGraphicsView):
    """Custom QGraphicsView that forwards mouse events to active tool"""

    def __init__(self, document, orchestrator):
        super().__init__(document.scene)
        self.document = document
        self.orchestrator = orchestrator
        
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        
        self.setBackgroundBrush(QBrush(QColor(128, 128, 128)))  # Gray background
        
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
        
        self.canvas_rect = canvas_rect
        self.max_zoom = 9.0  # Max zoom: each pixel appears as 9 screen pixels
        self.min_zoom = 0.1  # Will be recalculated in resizeEvent
    
    def reset_zoom_tracking(self):
        """Reset zoom tracking to 1.0 - call this after resetTransform or fitInView."""
        self.current_zoom = 1.0
    
    def resizeEvent(self, event):
        """Recalculate min_zoom when view is resized."""
        super().resizeEvent(event)
        
        if self.canvas_rect.width() > 0 and self.canvas_rect.height() > 0:
            viewport_rect = self.viewport().rect()
            
            zoom_x = viewport_rect.width() / self.canvas_rect.width()
            zoom_y = viewport_rect.height() / self.canvas_rect.height()
            
            self.min_zoom = min(zoom_x, zoom_y) * 0.95  # 95% to add small padding
            
            self.min_zoom = max(0.01, self.min_zoom)

    def mousePressEvent(self, event):
        """Forward mouse press to orchestrator"""
        self.orchestrator.handle_mouse_press(event, self.document.scene, self)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Forward mouse move to orchestrator"""
        self.orchestrator.handle_mouse_move(event, self.document.scene, self)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Forward mouse release to orchestrator and execute command if returned"""
        command = self.orchestrator.handle_mouse_release(event, self.document.scene, self)
        if command:
            self.document.execute_command(command)
            parent = self.window()
            if hasattr(parent, 'update_undo_redo_states'):
                parent.update_undo_redo_states()
        super().mouseReleaseEvent(event)
    
    def wheelEvent(self, event):
        """Handle mouse wheel - delegate to orchestrator."""
        handled = self.orchestrator.handle_wheel_event(event, self.document.scene, self)
        if not handled:
            super().wheelEvent(event)
