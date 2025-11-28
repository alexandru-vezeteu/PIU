from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QGroupBox, QAction)
from PyQt5.QtCore import Qt
from src.core.base_tool import BaseTool


class BucketTool(BaseTool):
    def __init__(self, color_callback=None, current_color=None):
        super().__init__("Paint Bucket", None)
        self.color_callback = color_callback
        self.current_color = current_color

    def create_action(self) -> QAction:
        self._action = QAction(self.name)
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        bucket_widget = QWidget()
        layout = QVBoxLayout(bucket_widget)

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
        color_layout.addWidget(QLabel("Fill Color:"))
        color_layout.addWidget(self.color_button)
        color_group.setLayout(color_layout)

        tolerance_label = QLabel("Tolerance: 30")
        self.tolerance_slider = QSlider(Qt.Horizontal)
        self.tolerance_slider.setRange(0, 100)
        self.tolerance_slider.setValue(30)
        self.tolerance_slider.valueChanged.connect(lambda val: tolerance_label.setText(f"Tolerance: {val}"))

        layout.addWidget(color_group)
        layout.addWidget(tolerance_label)
        layout.addWidget(self.tolerance_slider)
        layout.addStretch()

        self._settings_widget = bucket_widget
        return bucket_widget

    def get_tool_name(self) -> str:
        return "paint_bucket"

    def needs_color(self) -> bool:
        return True

    def update_color_display(self, color):
        if hasattr(self, 'color_button'):
            self.color_button.setStyleSheet(
                f"QPushButton {{ background-color: {color.name()}; border: 2px solid #666; }}"
            )
            self.color_button.update()

    def mouse_press_event(self, event, scene, view=None):
        pos = event.pos()
        tolerance = self.tolerance_slider.value()
        print(f"[Paint Bucket] Clicked at ({pos.x()}, {pos.y()}) - Tolerance: {tolerance}")

    def mouse_move_event(self, event, scene, view=None):
        pass

    def mouse_release_event(self, event, scene, view=None):
        pass
