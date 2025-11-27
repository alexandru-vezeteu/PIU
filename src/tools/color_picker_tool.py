from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QAction)
from src.core.base_tool import BaseTool


class ColorPickerTool(BaseTool):
    def __init__(self):
        super().__init__("Eyedropper", None)

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

    def mouse_press_event(self, event, scene):
        pos = event.pos()
        print(f"[Eyedropper] Picking color at ({pos.x()}, {pos.y()})")

    def mouse_move_event(self, event, scene):
        pass

    def mouse_release_event(self, event, scene):
        pass
