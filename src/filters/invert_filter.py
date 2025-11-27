from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QAction)
from PyQt5.QtGui import QImage
from src.core.base_filter import BaseFilter


class InvertFilter(BaseFilter):
    def __init__(self):
        super().__init__("Invert", None)

    def create_action(self) -> QAction:
        self._action = QAction(f"  {self.name}")
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        info_label = QLabel("Inverts all colors in the image.")
        info_label.setWordWrap(True)
        
        self.apply_btn = QPushButton("Apply Invert Filter")

        layout.addWidget(info_label)
        layout.addWidget(self.apply_btn)
        layout.addStretch()

        self._settings_widget = filter_widget
        return filter_widget

    def get_filter_name(self) -> str:
        return "invert"

    def apply_filter(self, image: QImage) -> QImage:
        """Apply invert filter to the image."""
        result = image.copy()
        
        result.invertPixels()
        
        return result
