from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpinBox,
                             QSlider, QAction)
from PyQt5.QtCore import Qt
from src.core.base_tool import BaseTool


class EraserTool(BaseTool):
    def __init__(self):
        super().__init__("Eraser", None)

    def create_action(self) -> QAction:
        self._action = QAction(self.name)
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

        hardness_label = QLabel("Hardness: 100%")
        self.hardness_slider = QSlider(Qt.Horizontal)
        self.hardness_slider.setRange(0, 100)
        self.hardness_slider.setValue(100)
        self.hardness_slider.valueChanged.connect(lambda val: hardness_label.setText(f"Hardness: {val}%"))

        layout.addWidget(QLabel("Size:"))
        layout.addWidget(size_label)
        layout.addWidget(self.size_spin)
        layout.addWidget(hardness_label)
        layout.addWidget(self.hardness_slider)
        layout.addStretch()

        self._settings_widget = eraser_widget
        return eraser_widget

    def get_tool_name(self) -> str:
        return "eraser"

    def mouse_press_event(self, event, scene):
        pos = event.pos()
        size = self.size_spin.value()
        print(f"[Eraser] Mouse pressed at ({pos.x()}, {pos.y()}) - Size: {size}")

    def mouse_move_event(self, event, scene):
        pos = event.pos()
        print(f"[Eraser] Erasing at ({pos.x()}, {pos.y()})")

    def mouse_release_event(self, event, scene):
        pos = event.pos()
        print(f"[Eraser] Mouse released at ({pos.x()}, {pos.y()})")
