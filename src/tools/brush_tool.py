from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpinBox,
                             QSlider, QPushButton, QGroupBox, QAction)
from PyQt5.QtCore import Qt
from src.core.base_tool import BaseTool


class BrushTool(BaseTool):
    def __init__(self, tool_type="paintbrush", color_callback=None, current_color=None):
        super().__init__(tool_type.capitalize(), icon_path=None)
        self.tool_type = tool_type
        self.color_callback = color_callback
        self.current_color = current_color

    def create_action(self) -> QAction:
        from PyQt5.QtGui import QIcon
        if self.icon_path:
            self._action = QAction(QIcon(self.icon_path), self.name, None)
        else:
            self._action = QAction(self.name)
        self._action.setCheckable(True)
        if self.tool_type == "paintbrush":
            self._action.setChecked(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        brush_widget = QWidget()
        layout = QVBoxLayout(brush_widget)

        size_label = QLabel("Brush Size: 5")
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 100)
        self.size_spin.setValue(5)
        self.size_spin.valueChanged.connect(lambda val: size_label.setText(f"Brush Size: {val}"))

        opacity_label = QLabel("Opacity: 100%")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(lambda val: opacity_label.setText(f"Opacity: {val}%"))

        hardness_label = QLabel("Hardness: 100%")
        self.hardness_slider = QSlider(Qt.Horizontal)
        self.hardness_slider.setRange(0, 100)
        self.hardness_slider.setValue(100)
        self.hardness_slider.valueChanged.connect(lambda val: hardness_label.setText(f"Hardness: {val}%"))

        layout.addWidget(QLabel("Size:"))
        layout.addWidget(size_label)
        layout.addWidget(self.size_spin)
        layout.addWidget(opacity_label)
        layout.addWidget(self.opacity_slider)
        layout.addWidget(hardness_label)
        layout.addWidget(self.hardness_slider)
        layout.addStretch()

        self._settings_widget = brush_widget
        return brush_widget

    def get_tool_name(self) -> str:
        return self.tool_type

    def needs_color(self) -> bool:
        return True

    def mouse_press_event(self, event, scene, view=None):
        """Start a new stroke."""
        from PyQt5.QtWidgets import QGraphicsPathItem
        from PyQt5.QtGui import QPainterPath, QPen
        from PyQt5.QtCore import Qt
        
        if view:
            pos = view.mapToScene(event.pos())
        else:
            pos = event.pos()
        
        size = self.size_spin.value()
        opacity = self.opacity_slider.value() / 100.0
        
        self.current_path = QPainterPath()
        self.current_path.moveTo(pos)
        
        pen = QPen(self.current_color if hasattr(self, 'current_color') else Qt.black)
        pen.setWidth(size)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        
        self.current_item = QGraphicsPathItem(self.current_path)
        self.current_item.setPen(pen)
        self.current_item.setOpacity(opacity)
        
        scene.addItem(self.current_item)
        
        print(f"[{self.tool_type.capitalize()}] Started stroke at ({pos.x():.1f}, {pos.y():.1f})")

    def mouse_move_event(self, event, scene, view=None):
        """Continue the stroke."""
        if hasattr(self, 'current_item') and self.current_item:
            if view:
                pos = view.mapToScene(event.pos())
            else:
                pos = event.pos()
            
            self.current_path.lineTo(pos)
            self.current_item.setPath(self.current_path)

    def mouse_release_event(self, event, scene, view=None):
        """Finish the stroke and create a command."""
        from src.commands.draw_command import DrawCommand
        
        if view:
            pos = view.mapToScene(event.pos())
        else:
            pos = event.pos()
        
        print(f"[{self.tool_type.capitalize()}] Finished stroke at ({pos.x():.1f}, {pos.y():.1f})")
        
        if hasattr(self, 'current_item') and self.current_item:
            scene.removeItem(self.current_item)
            
            command = DrawCommand(
                self.current_item,
                f"{self.tool_type.capitalize()} Stroke"
            )
            
            self.current_item = None
            self.current_path = None
            
            return command
        
        return None
