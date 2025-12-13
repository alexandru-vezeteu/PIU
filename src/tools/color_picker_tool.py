from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QAction)
from PyQt5.QtGui import QColor
from src.core.base_tool import BaseTool


class ColorPickerTool(BaseTool):
    def __init__(self):
        super().__init__("Eyedropper", None)
        self.color_picker_widget = None

    def set_color_picker_widget(self, widget):
        """Set reference to the color picker widget for updating colors."""
        self.color_picker_widget = widget

    def create_action(self) -> QAction:
        self._action = QAction(self.name)
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        picker_widget = QWidget()
        layout = QVBoxLayout(picker_widget)

        info_label = QLabel("Click on the image to pick a color.\nThe selected color will be set as the current color.")
        info_label.setWordWrap(True)

        layout.addWidget(info_label)
        layout.addStretch()

        self._settings_widget = picker_widget
        return picker_widget

    def get_tool_name(self) -> str:
        return "color_picker"

    def mouse_press_event(self, event, scene, view=None):
        if view:
            scene_pos = view.mapToScene(event.pos())
        else:
            scene_pos = event.pos()
        
        x = int(scene_pos.x())
        y = int(scene_pos.y())
        
        canvas_item = None
        for item in scene.items():
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if not canvas_item:
            print(f"[Eyedropper] No canvas found")
            return
        
        canvas_image = canvas_item.pixmap().toImage()
        
        if x < 0 or y < 0 or x >= canvas_image.width() or y >= canvas_image.height():
            print(f"[Eyedropper] Click outside canvas bounds")
            return
        
        pixel_color = canvas_image.pixelColor(x, y)
        
        print(f"[Eyedropper] Picked color {pixel_color.name()} at ({x}, {y})")
        
        if self.color_picker_widget:
            self.color_picker_widget.set_color(pixel_color)

    def mouse_move_event(self, event, scene, view=None):
        pass

    def mouse_release_event(self, event, scene, view=None):
        pass
