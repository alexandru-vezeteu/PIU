from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpinBox,
                             QPushButton, QGroupBox, QComboBox, QAction)
from src.core.base_tool import BaseTool


class ShapeTool(BaseTool):
    def __init__(self, shape_type, color_callback=None, current_color=None):
        names = {
            "rectangle": "Rectangle",
            "circle": "Circle/Ellipse",
            "line": "Line"
        }
        super().__init__(names.get(shape_type, shape_type), None)
        self.shape_type = shape_type
        self.color_callback = color_callback
        self.current_color = current_color

    def create_action(self) -> QAction:
        self._action = QAction(self.name)
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        shape_widget = QWidget()
        layout = QVBoxLayout(shape_widget)

        self.fill_combo = QComboBox()
        self.fill_combo.addItems(["Stroke Only", "Fill Only", "Stroke + Fill"])

        width_label = QLabel("Line Width: 2")
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 50)
        self.width_spin.setValue(2)
        self.width_spin.valueChanged.connect(lambda val: width_label.setText(f"Line Width: {val}"))

        layout.addWidget(QLabel("Draw Mode:"))
        layout.addWidget(self.fill_combo)
        layout.addWidget(width_label)
        layout.addWidget(self.width_spin)
        layout.addStretch()

        self._settings_widget = shape_widget
        return shape_widget

    def get_tool_name(self) -> str:
        return self.shape_type

    def needs_color(self) -> bool:
        return True

    def mouse_press_event(self, event, scene, view=None):
        pos = event.pos()
        mode = self.fill_combo.currentText()
        print(f"[{self.shape_type.capitalize()}] Mouse pressed at ({pos.x()}, {pos.y()}) - Mode: {mode}")

    def mouse_move_event(self, event, scene, view=None):
        pos = event.pos()
        print(f"[{self.shape_type.capitalize()}] Drawing shape to ({pos.x()}, {pos.y()})")

    def mouse_release_event(self, event, scene, view=None):
        pos = event.pos()
        print(f"[{self.shape_type.capitalize()}] Shape completed at ({pos.x()}, {pos.y()})")
