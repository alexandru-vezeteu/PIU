from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter


class CanvasView(QGraphicsView):
    """Custom QGraphicsView that forwards mouse events to active tool"""

    def __init__(self, scene, tool_manager):
        super().__init__(scene)
        self.tool_manager = tool_manager
        self.setRenderHint(QPainter.Antialiasing)

    def mousePressEvent(self, event):
        """Forward mouse press to active tool"""
        current_tool = self.tool_manager.get_current_tool()
        if current_tool:
            current_tool.mouse_press_event(event, self.scene())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Forward mouse move to active tool"""
        current_tool = self.tool_manager.get_current_tool()
        if current_tool:
            current_tool.mouse_move_event(event, self.scene())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Forward mouse release to active tool"""
        current_tool = self.tool_manager.get_current_tool()
        if current_tool:
            current_tool.mouse_release_event(event, self.scene())
        super().mouseReleaseEvent(event)
