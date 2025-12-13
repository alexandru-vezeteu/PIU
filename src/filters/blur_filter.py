from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QComboBox, QAction)
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
    return qimage.copy()  


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

        self.apply_btn = QPushButton("Apply Filter")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(lambda: self.radius_slider.setValue(5))

        layout.addWidget(blur_type_label)
        layout.addWidget(self.blur_type_combo)
        layout.addWidget(radius_label)
        layout.addWidget(self.radius_slider)
        layout.addWidget(self.apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self._settings_widget = filter_widget
        return filter_widget

    def get_filter_name(self) -> str:
        return "blur"

    def apply_filter(self, image: QImage) -> QImage:
        """Apply blur filter to the image."""
        blur_type = self.blur_type_combo.currentText()
        radius = self.radius_slider.value()
        
        pil_image = qimage_to_pil(image)
        
        if pil_image.mode == "RGBA":
            r, g, b, a = pil_image.split()
            rgb_image = Image.merge("RGB", (r, g, b))
        else:
            rgb_image = pil_image.convert("RGB")
            a = None
        
        if blur_type == "Gaussian Blur":
            blurred = rgb_image.filter(ImageFilter.GaussianBlur(radius=radius))
        elif blur_type == "Box Blur":
            blurred = rgb_image.filter(ImageFilter.BoxBlur(radius=radius))
        elif blur_type == "Motion Blur":
            kernel_size = radius * 2 + 1
            kernel = [0] * (kernel_size * kernel_size)
            middle_row = kernel_size // 2
            for i in range(kernel_size):
                kernel[middle_row * kernel_size + i] = 1
            kernel_sum = sum(kernel)
            kernel = [k / kernel_sum for k in kernel]
            blurred = rgb_image.filter(
                ImageFilter.Kernel(
                    size=(kernel_size, kernel_size),
                    kernel=kernel,
                    scale=1,
                    offset=0
                )
            )
        else:
            blurred = rgb_image
        
        if a is not None:
            result = Image.merge("RGBA", (*blurred.split(), a))
        else:
            result = blurred.convert("RGBA")
        
        return pil_to_qimage(result)
