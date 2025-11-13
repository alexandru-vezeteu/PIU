from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QComboBox, QAction)
from PyQt5.QtCore import Qt
from src.core.base_filter import BaseFilter


class BlurFilter(BaseFilter):
    def __init__(self):
        super().__init__("Blur", None)

    def create_action(self) -> QAction:
        self._action = QAction(f"  {self.name}")
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        blur_type_label = QLabel("Blur Type:")
        self.blur_type_combo = QComboBox()
        self.blur_type_combo.addItems(["Gaussian Blur", "Motion Blur", "Box Blur"])

        radius_label = QLabel("Radius: 5")
        self.radius_slider = QSlider(Qt.Horizontal)
        self.radius_slider.setRange(1, 50)
        self.radius_slider.setValue(5)
        self.radius_slider.valueChanged.connect(lambda val: radius_label.setText(f"Radius: {val}"))

        apply_btn = QPushButton("Apply Filter")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(lambda: self.radius_slider.setValue(5))

        layout.addWidget(blur_type_label)
        layout.addWidget(self.blur_type_combo)
        layout.addWidget(radius_label)
        layout.addWidget(self.radius_slider)
        layout.addWidget(apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self._settings_widget = filter_widget
        return filter_widget

    def get_filter_name(self) -> str:
        return "blur"

    def apply_filter(self, image):
        pass
