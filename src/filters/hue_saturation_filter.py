from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from PIL import Image
import numpy as np
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

        self.apply_btn = QPushButton("Apply Filter")
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
        layout.addWidget(self.apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self._settings_widget = filter_widget
        return filter_widget

    def get_filter_name(self) -> str:
        return "hue_saturation"

    def apply_filter(self, image: QImage) -> QImage:
        """Apply hue, saturation, and lightness adjustments to the image."""
        hue_shift = self.hue_slider.value()
        saturation_adjust = self.saturation_slider.value()
        lightness_adjust = self.lightness_slider.value()
        
        if hue_shift == 0 and saturation_adjust == 0 and lightness_adjust == 0:
            return image
        
        pil_image = qimage_to_pil(image)
        
        if pil_image.mode == "RGBA":
            r, g, b, a = pil_image.split()
            rgb_image = Image.merge("RGB", (r, g, b))
        else:
            rgb_image = pil_image.convert("RGB")
            a = None
        
        hsv_image = rgb_image.convert("HSV")
        
        hsv_array = np.array(hsv_image, dtype=np.float32)
        
        hue_shift_scaled = (hue_shift / 180.0) * 128.0
        hsv_array[:, :, 0] = (hsv_array[:, :, 0] + hue_shift_scaled) % 256
        
        if saturation_adjust > 0:
            saturation_factor = 1.0 + (saturation_adjust / 100.0)
            hsv_array[:, :, 1] = np.clip(hsv_array[:, :, 1] * saturation_factor, 0, 255)
        else:
            saturation_factor = 1.0 + (saturation_adjust / 100.0)  
            hsv_array[:, :, 1] = hsv_array[:, :, 1] * saturation_factor
        
        if lightness_adjust > 0:
            lightness_factor = 1.0 + (lightness_adjust / 100.0)
            hsv_array[:, :, 2] = np.clip(hsv_array[:, :, 2] * lightness_factor, 0, 255)
        else:
            lightness_factor = 1.0 + (lightness_adjust / 100.0)  
            hsv_array[:, :, 2] = hsv_array[:, :, 2] * lightness_factor
        
        hsv_array = hsv_array.astype(np.uint8)
        
        hsv_result = Image.fromarray(hsv_array, mode="HSV")
        
        rgb_result = hsv_result.convert("RGB")
        
        if a is not None:
            result = Image.merge("RGBA", (*rgb_result.split(), a))
        else:
            result = rgb_result.convert("RGBA")
        
        return pil_to_qimage(result)
