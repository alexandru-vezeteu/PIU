from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QAction)
from PyQt5.QtCore import Qt
from src.core.base_filter import BaseFilter


class SharpenFilter(BaseFilter):
    def __init__(self):
        super().__init__("Sharpen", None)

    def create_action(self) -> QAction:
        self._action = QAction(f"  {self.name}")
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        amount_label = QLabel("Amount: 50%")
        self.amount_slider = QSlider(Qt.Horizontal)
        self.amount_slider.setRange(0, 100)
        self.amount_slider.setValue(50)
        self.amount_slider.valueChanged.connect(lambda val: amount_label.setText(f"Amount: {val}%"))

        apply_btn = QPushButton("Apply Filter")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(lambda: self.amount_slider.setValue(50))

        layout.addWidget(amount_label)
        layout.addWidget(self.amount_slider)
        layout.addWidget(apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self._settings_widget = filter_widget
        return filter_widget

    def get_filter_name(self) -> str:
        return "sharpen"

    def apply_filter(self, image):
        pass
