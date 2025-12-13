from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from PIL import Image, ImageFilter
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
    return qimage.copy()  # Make a deep copy to own the data


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

        self.apply_btn = QPushButton("Apply Filter")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(lambda: self.amount_slider.setValue(50))

        layout.addWidget(amount_label)
        layout.addWidget(self.amount_slider)
        layout.addWidget(self.apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self._settings_widget = filter_widget
        return filter_widget

    def get_filter_name(self) -> str:
        return "sharpen"

    def apply_filter(self, image: QImage) -> QImage:
        """Apply sharpen filter to the image using UnsharpMask."""
        amount = self.amount_slider.value()
        
        if amount == 0:
            return image
        
        pil_image = qimage_to_pil(image)
        
        if pil_image.mode == "RGBA":
            r, g, b, a = pil_image.split()
            rgb_image = Image.merge("RGB", (r, g, b))
        else:
            rgb_image = pil_image.convert("RGB")
            a = None
        
        percent = amount * 2
        
        sharpened = rgb_image.filter(
            ImageFilter.UnsharpMask(radius=2, percent=percent, threshold=3)
        )
        
        if a is not None:
            result = Image.merge("RGBA", (*sharpened.split(), a))
        else:
            result = sharpened.convert("RGBA")
        
        return pil_to_qimage(result)
