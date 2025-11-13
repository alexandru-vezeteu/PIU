from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QAction)
from PyQt5.QtCore import Qt
from src.core.base_filter import BaseFilter


class BrightnessContrastFilter(BaseFilter):
    def __init__(self):
        super().__init__("Brightness/Contrast", None)

    def create_action(self) -> QAction:
        self._action = QAction(f"  {self.name}")
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        self.brightness_label = QLabel("Brightness: 0")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(
            lambda val: self.brightness_label.setText(f"Brightness: {val}")
        )

        self.contrast_label = QLabel("Contrast: 0")
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(-100, 100)
        self.contrast_slider.setValue(0)
        self.contrast_slider.valueChanged.connect(
            lambda val: self.contrast_label.setText(f"Contrast: {val}")
        )

        apply_btn = QPushButton("Apply Filter")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(
            lambda: (self.brightness_slider.setValue(0), self.contrast_slider.setValue(0))
        )

        layout.addWidget(QLabel("Brightness:"))
        layout.addWidget(self.brightness_label)
        layout.addWidget(self.brightness_slider)
        layout.addWidget(QLabel("Contrast:"))
        layout.addWidget(self.contrast_label)
        layout.addWidget(self.contrast_slider)
        layout.addWidget(apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self._settings_widget = filter_widget
        return filter_widget

    def get_filter_name(self) -> str:
        return "brightness_contrast"

    def apply_filter(self, image):
        pass
