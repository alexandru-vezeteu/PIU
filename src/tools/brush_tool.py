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
    
    def get_key_binding(self) -> str:
        """Return keyboard shortcut."""
        if self.tool_type == "paintbrush":
            return "B"
        return None

    def create_settings_panel(self) -> QWidget:
        brush_widget = QWidget()
        layout = QVBoxLayout(brush_widget)

        size_label = QLabel("Brush Size: 5")
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 100)
        self.size_spin.setValue(5)
        
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(1, 100)
        self.size_slider.setValue(5)
        
        def update_size(val):
            size_label.setText(f"Brush Size: {val}")
            self.size_spin.setValue(val)
            self.size_slider.setValue(val)
        
        self.size_spin.valueChanged.connect(update_size)
        self.size_slider.valueChanged.connect(update_size)

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

        layout.addWidget(size_label)
        layout.addWidget(self.size_slider)
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
        """Start a new stroke - capture initial canvas state."""
        
        if view:
            pos = view.mapToScene(event.pos())
        else:
            pos = event.pos()
        
        self.view = view
        
        self.last_pos = pos
        
        self.before_image = None
        
        print(f"[{self.tool_type.capitalize()}] Started stroke at ({pos.x():.1f}, {pos.y():.1f})")

    def mouse_move_event(self, event, scene, view=None):
        """Continue the stroke - draw directly to canvas pixels."""
        if not hasattr(self, 'last_pos') or self.last_pos is None:
            return
            
        if view:
            current_pos = view.mapToScene(event.pos())
        else:
            current_pos = event.pos()
        
        from PyQt5.QtGui import QPainter, QPen, QPixmap, QBrush
        import random
        
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
        opacity = self.opacity_slider.value() / 100.0
        
        color = self.current_color if hasattr(self, 'current_color') and self.current_color else Qt.black
        
        if self.tool_type == "airbrush":
            painter.setOpacity(opacity * 0.3)
            num_dots = max(5, size // 2)
            for _ in range(num_dots):
                offset_x = random.gauss(0, size / 3)
                offset_y = random.gauss(0, size / 3)
                dot_x = current_pos.x() + offset_x
                dot_y = current_pos.y() + offset_y
                dot_size = random.randint(1, max(2, size // 4))
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawEllipse(int(dot_x), int(dot_y), dot_size, dot_size)
        else:
            pen = QPen(color)
            pen.setWidth(size)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            painter.setOpacity(opacity)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawLine(self.last_pos, current_pos)
        
        painter.end()
        
        canvas_item.setPixmap(pixmap)
        
        self.last_pos = current_pos

    def mouse_release_event(self, event, scene, view=None):
        """Finish the stroke and create a command."""
        from src.commands.pixel_draw_command import PixelDrawCommand
        
        if view:
            pos = view.mapToScene(event.pos())
        else:
            pos = event.pos()
        
        print(f"[{self.tool_type.capitalize()}] Finished stroke at ({pos.x():.1f}, {pos.y():.1f})")
        
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
                    f"{self.tool_type.capitalize()} Stroke"
                )
                
                self.before_image = None
                self.last_pos = None
                
                return command
        
        self.before_image = None
        self.last_pos = None
        
        return None

