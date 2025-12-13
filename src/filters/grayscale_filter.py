from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QAction)
from PyQt5.QtGui import QImage
from PIL import Image, ImageOps
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


class GrayscaleFilter(BaseFilter):
    def __init__(self):
        super().__init__("Grayscale", None)

    def create_action(self) -> QAction:
        self._action = QAction(f"  {self.name}")
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        info_label = QLabel("Converts the image to grayscale.\nNo additional settings required.")
        info_label.setWordWrap(True)

        self.apply_btn = QPushButton("Apply Filter")

        layout.addWidget(info_label)
        layout.addWidget(self.apply_btn)
        layout.addStretch()

        self._settings_widget = filter_widget
        return filter_widget

    def get_filter_name(self) -> str:
        return "grayscale"

    def apply_filter(self, image: QImage) -> QImage:
        """Apply grayscale filter to the image, preserving alpha channel."""
        pil_image = qimage_to_pil(image)
        
        if pil_image.mode == "RGBA":
            r, g, b, a = pil_image.split()
            rgb_image = Image.merge("RGB", (r, g, b))
            gray_image = ImageOps.grayscale(rgb_image)
            result = Image.merge("RGBA", (gray_image, gray_image, gray_image, a))
        else:
            result = ImageOps.grayscale(pil_image).convert("RGBA")
        
        return pil_to_qimage(result)
