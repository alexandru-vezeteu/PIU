from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpinBox,
                             QSlider, QPushButton, QGroupBox, QAction)
from PyQt5.QtCore import Qt
from src.core.base_tool import BaseTool


class BrushTool(BaseTool):
    def __init__(self, tool_type="paintbrush", color_callback=None, current_color=None):
        icon_path = "assets/icons/paint_brush.png" if tool_type == "paintbrush" else None
        super().__init__(tool_type.capitalize(), icon_path)
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

        color_group = QGroupBox("Color")
        color_layout = QVBoxLayout()
        self.color_button = QPushButton()
        self.color_button.setFixedSize(100, 30)
        if self.current_color:
            self.color_button.setStyleSheet(
                f"QPushButton {{ background-color: {self.current_color.name()}; border: 2px solid #666; }}"
            )
        if self.color_callback:
            self.color_button.clicked.connect(self.color_callback)
        color_layout.addWidget(QLabel("Current Color:"))
        color_layout.addWidget(self.color_button)
        color_group.setLayout(color_layout)

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

        layout.addWidget(color_group)
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

    def update_color_display(self, color):
        if hasattr(self, 'color_button'):
            self.color_button.setStyleSheet(
                f"QPushButton {{ background-color: {color.name()}; border: 2px solid #666; }}"
            )
            self.color_button.update()

    def mouse_press_event(self, event, scene):
        pos = event.pos()
        size = self.size_spin.value()
        opacity = self.opacity_slider.value()
        print(f"[{self.tool_type.capitalize()}] Mouse pressed at ({pos.x()}, {pos.y()}) - Size: {size}, Opacity: {opacity}%")

    def mouse_move_event(self, event, scene):
        pos = event.pos()
        print(f"[{self.tool_type.capitalize()}] Painting at ({pos.x()}, {pos.y()})")

    def mouse_release_event(self, event, scene):
        pos = event.pos()
        print(f"[{self.tool_type.capitalize()}] Mouse released at ({pos.x()}, {pos.y()})")
