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
        """Start a new erase stroke."""
        from PyQt5.QtWidgets import QGraphicsPathItem
        from PyQt5.QtGui import QPainterPath, QPen
        
        if view:
            pos = view.mapToScene(event.pos())
        else:
            pos = event.pos()
        
        size = self.size_spin.value()
        
        self.current_path = QPainterPath()
        self.current_path.moveTo(pos)
        
        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(size)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        
        self.current_item = QGraphicsPathItem(self.current_path)
        self.current_item.setPen(pen)
        
        scene.addItem(self.current_item)

    def mouse_move_event(self, event, scene, view=None):
        """Continue the erase stroke."""
        if hasattr(self, 'current_item') and self.current_item:
            if view:
                pos = view.mapToScene(event.pos())
            else:
                pos = event.pos()
            
            self.current_path.lineTo(pos)
            self.current_item.setPath(self.current_path)

    def mouse_release_event(self, event, scene, view=None):
        """Finish the erase stroke and create a command."""
        from src.commands.draw_command import DrawCommand
        
        if hasattr(self, 'current_item') and self.current_item:
            scene.removeItem(self.current_item)
            
            command = DrawCommand(
                self.current_item,
                "Eraser Stroke"
            )
            
            self.current_item = None
            self.current_path = None
            
            return command
        
        return None
