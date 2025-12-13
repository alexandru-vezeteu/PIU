from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QGroupBox, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QColor, QPixmap
from src.core.base_tool import BaseTool
import numpy as np
import cv2


class BucketTool(BaseTool):
    def __init__(self, color_callback=None, current_color=None):
        super().__init__("Paint Bucket", None)
        self.color_callback = color_callback
        self.current_color = current_color

    def create_action(self) -> QAction:
        self._action = QAction(self.name)
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        bucket_widget = QWidget()
        layout = QVBoxLayout(bucket_widget)

        tolerance_label = QLabel("Tolerance: 30")
        self.tolerance_slider = QSlider(Qt.Horizontal)
        self.tolerance_slider.setRange(0, 100)
        self.tolerance_slider.setValue(30)
        self.tolerance_slider.valueChanged.connect(lambda val: tolerance_label.setText(f"Tolerance: {val}"))

        layout.addWidget(tolerance_label)
        layout.addWidget(self.tolerance_slider)
        layout.addStretch()

        self._settings_widget = bucket_widget
        return bucket_widget

    def get_tool_name(self) -> str:
        return "paint_bucket"

    def needs_color(self) -> bool:
        return True

    def _qimage_to_numpy(self, image: QImage) -> np.ndarray:
        image = image.convertToFormat(QImage.Format_RGBA8888)
        ptr = image.bits()
        ptr.setsize(image.height() * image.width() * 4)
        return np.frombuffer(ptr, dtype=np.uint8).reshape((image.height(), image.width(), 4)).copy()

    def _numpy_to_qimage(self, arr: np.ndarray) -> QImage:
        h, w, _ = arr.shape
        return QImage(arr.data, w, h, w * 4, QImage.Format_RGBA8888).copy()

    def mouse_press_event(self, event, scene, view=None):
        from src.commands.pixel_draw_command import PixelDrawCommand
        
        if view:
            scene_pos = view.mapToScene(event.pos())
        else:
            scene_pos = event.pos()
        
        x = int(scene_pos.x())
        y = int(scene_pos.y())
        tolerance = self.tolerance_slider.value()
        
        canvas_item = None
        for item in scene.items():
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if not canvas_item:
            print(f"[Paint Bucket] No canvas found")
            return
        
        before_image = canvas_item.pixmap().toImage().copy()
        
        if x < 0 or y < 0 or x >= before_image.width() or y >= before_image.height():
            print(f"[Paint Bucket] Click outside canvas bounds")
            return
        
        fill_color = self.current_color if self.current_color else QColor(0, 0, 0)
        
        print(f"[Paint Bucket] Filling at ({x}, {y}) with {fill_color.name()} - Tolerance: {tolerance}")
        
        arr = self._qimage_to_numpy(before_image)
        rgb = arr[:, :, :3].copy()
        
        mask = np.zeros((rgb.shape[0] + 2, rgb.shape[1] + 2), np.uint8)
        new_color = (fill_color.red(), fill_color.green(), fill_color.blue())
        
        cv2.floodFill(rgb, mask, (x, y), new_color,
                      loDiff=(tolerance, tolerance, tolerance),
                      upDiff=(tolerance, tolerance, tolerance),
                      flags=4 | cv2.FLOODFILL_FIXED_RANGE | (255 << 8))
        
        arr[:, :, :3] = rgb
        arr[:, :, 3][mask[1:-1, 1:-1] == 255] = fill_color.alpha()
        
        after_image = self._numpy_to_qimage(arr)
        
        canvas_item.setPixmap(QPixmap.fromImage(after_image))
        
        self._pending_command = PixelDrawCommand(before_image, after_image, "Paint Bucket Fill")

    def mouse_move_event(self, event, scene, view=None):
        pass

    def mouse_release_event(self, event, scene, view=None):
        if hasattr(self, '_pending_command') and self._pending_command:
            command = self._pending_command
            self._pending_command = None
            return command
        return None
