from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpinBox,
                             QSlider, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from src.core.base_tool import BaseTool


class EraserTool(BaseTool):
    def __init__(self):
        super().__init__("Eraser", icon_path=None)

    def create_action(self) -> QAction:
        self._action = QAction("Eraser")
        self._action.setCheckable(True)
        return self._action
    
    def get_key_binding(self) -> str:
        """Return keyboard shortcut."""
        return "E"

    def create_settings_panel(self) -> QWidget:
        eraser_widget = QWidget()
        layout = QVBoxLayout(eraser_widget)

        size_label = QLabel("Eraser Size: 10")
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 100)
        self.size_spin.setValue(10)
        self.size_spin.valueChanged.connect(lambda val: size_label.setText(f"Eraser Size: {val}"))

        layout.addWidget(QLabel("Size:"))
        layout.addWidget(size_label)
        layout.addWidget(self.size_spin)
        layout.addStretch()

        self._settings_widget = eraser_widget
        return eraser_widget

    def get_tool_name(self) -> str:
        return "eraser"

    def mouse_press_event(self, event, scene, view=None):
        """Start a new erase stroke - capture initial canvas state."""
        
        if view:
            pos = view.mapToScene(event.pos())
        else:
            pos = event.pos()
        
        self.last_pos = pos
        
        self.before_image = None

    def mouse_move_event(self, event, scene, view=None):
        """Continue the erase stroke - draw white directly to canvas pixels."""
        if not hasattr(self, 'last_pos') or self.last_pos is None:
            return
            
        if view:
            current_pos = view.mapToScene(event.pos())
        else:
            current_pos = event.pos()
        
        from PyQt5.QtGui import QPainter, QPen
        
        canvas_item = None
        for item in scene.items():
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if not canvas_item:
            return
        
        if self.before_image is None:
            self.before_image = canvas_item.pixmap().toImage().copy()
        
        pixmap = canvas_item.pixmap()
        painter = QPainter(pixmap)
        
        size = self.size_spin.value()
        
        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(size)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.drawLine(self.last_pos, current_pos)
        
        painter.end()
        
        canvas_item.setPixmap(pixmap)
        
        self.last_pos = current_pos

    def mouse_release_event(self, event, scene, view=None):
        """Finish the erase stroke and create a command."""
        from src.commands.pixel_draw_command import PixelDrawCommand
        
        if hasattr(self, 'before_image') and self.before_image is not None:
            canvas_item = None
            for item in scene.items():
                if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                    canvas_item = item
                    break
            
            if canvas_item:
                after_image = canvas_item.pixmap().toImage().copy()
                
                command = PixelDrawCommand(
                    self.before_image,
                    after_image,
                    "Eraser Stroke"
                )
                
                self.before_image = None
                self.last_pos = None
                
                return command
        
        self.before_image = None
        self.last_pos = None
        
        return None

