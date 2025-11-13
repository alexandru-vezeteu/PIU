from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QAction)
from PyQt5.QtCore import Qt
from src.core.base_filter import BaseFilter


class HueSaturationFilter(BaseFilter):
    def __init__(self):
        super().__init__("Hue/Saturation", None)

    def create_action(self) -> QAction:
        self._action = QAction(f"  {self.name}")
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        hue_label = QLabel("Hue: 0")
        self.hue_slider = QSlider(Qt.Horizontal)
        self.hue_slider.setRange(-180, 180)
        self.hue_slider.setValue(0)
        self.hue_slider.valueChanged.connect(lambda val: hue_label.setText(f"Hue: {val}"))

        saturation_label = QLabel("Saturation: 0")
        self.saturation_slider = QSlider(Qt.Horizontal)
        self.saturation_slider.setRange(-100, 100)
        self.saturation_slider.setValue(0)
        self.saturation_slider.valueChanged.connect(lambda val: saturation_label.setText(f"Saturation: {val}"))

        lightness_label = QLabel("Lightness: 0")
        self.lightness_slider = QSlider(Qt.Horizontal)
        self.lightness_slider.setRange(-100, 100)
        self.lightness_slider.setValue(0)
        self.lightness_slider.valueChanged.connect(lambda val: lightness_label.setText(f"Lightness: {val}"))

        apply_btn = QPushButton("Apply Filter")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(
            lambda: (self.hue_slider.setValue(0), self.saturation_slider.setValue(0), self.lightness_slider.setValue(0))
        )

        layout.addWidget(hue_label)
        layout.addWidget(self.hue_slider)
        layout.addWidget(saturation_label)
        layout.addWidget(self.saturation_slider)
        layout.addWidget(lightness_label)
        layout.addWidget(self.lightness_slider)
        layout.addWidget(apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self._settings_widget = filter_widget
        return filter_widget

    def get_filter_name(self) -> str:
        return "hue_saturation"

    def apply_filter(self, image):
        pass
