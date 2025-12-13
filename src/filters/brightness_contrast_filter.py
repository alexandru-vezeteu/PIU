from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from PIL import Image, ImageEnhance
from src.core.base_filter import BaseFilter


def qimage_to_pil(qimage: QImage) -> Image.Image:
    """Convert QImage to PIL Image."""
    qimage = qimage.convertToFormat(QImage.Format_RGBA8888)
    width = qimage.width()
    height = qimage.height()
    ptr = qimage.bits()
    ptr.setsize(height * width * 4)
    return Image.frombytes("RGBA", (width, height), bytes(ptr), "raw", "RGBA")


def pil_to_qimage(pil_image: Image.Image) -> QImage:
    """Convert PIL Image to QImage."""
    if pil_image.mode != "RGBA":
        pil_image = pil_image.convert("RGBA")
    data = pil_image.tobytes("raw", "RGBA")
    qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
    return qimage.copy()  


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

        self.apply_btn = QPushButton("Apply Filter")
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
        layout.addWidget(self.apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self._settings_widget = filter_widget
        return filter_widget

    def get_filter_name(self) -> str:
        return "brightness_contrast"

    def apply_filter(self, image: QImage) -> QImage:
        """Apply brightness and contrast adjustments to the image."""
        brightness_value = self.brightness_slider.value()
        contrast_value = self.contrast_slider.value()
        
        pil_image = qimage_to_pil(image)
        
        if pil_image.mode == "RGBA":
            r, g, b, a = pil_image.split()
            rgb_image = Image.merge("RGB", (r, g, b))
        else:
            rgb_image = pil_image.convert("RGB")
            a = None
        
        brightness_factor = (brightness_value + 100) / 100.0
        contrast_factor = (contrast_value + 100) / 100.0
        
        if brightness_value != 0:
            enhancer = ImageEnhance.Brightness(rgb_image)
            rgb_image = enhancer.enhance(brightness_factor)
        
        if contrast_value != 0:
            enhancer = ImageEnhance.Contrast(rgb_image)
            rgb_image = enhancer.enhance(contrast_factor)
        
        if a is not None:
            result = Image.merge("RGBA", (*rgb_image.split(), a))
        else:
            result = rgb_image.convert("RGBA")
        
        return pil_to_qimage(result)
