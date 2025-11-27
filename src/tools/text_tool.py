from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpinBox,
                             QPushButton, QGroupBox, QComboBox, QAction)
from src.core.base_tool import BaseTool


class TextTool(BaseTool):
    def __init__(self, color_callback=None, current_color=None):
        super().__init__("Text", None)
        self.color_callback = color_callback
        self.current_color = current_color

    def create_action(self) -> QAction:
        self._action = QAction(self.name)
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        text_widget = QWidget()
        layout = QVBoxLayout(text_widget)

        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "Courier New", "Helvetica", "Comic Sans MS"])

        size_label = QLabel("Font Size: 12")
        self.size_spin = QSpinBox()
        self.size_spin.setRange(6, 144)
        self.size_spin.setValue(12)
        self.size_spin.valueChanged.connect(lambda val: size_label.setText(f"Font Size: {val}"))

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
        color_layout.addWidget(QLabel("Text Color:"))
        color_layout.addWidget(self.color_button)
        color_group.setLayout(color_layout)

        layout.addWidget(QLabel("Font:"))
        layout.addWidget(self.font_combo)
        layout.addWidget(size_label)
        layout.addWidget(self.size_spin)
        layout.addWidget(color_group)
        layout.addStretch()

        self._settings_widget = text_widget
        return text_widget

    def get_tool_name(self) -> str:
        return "text"

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
        font = self.font_combo.currentText()
        size = self.size_spin.value()
        print(f"[Text] Clicked at ({pos.x()}, {pos.y()}) - Font: {font}, Size: {size}")

    def mouse_move_event(self, event, scene):
        pass

    def mouse_release_event(self, event, scene):
        pass
