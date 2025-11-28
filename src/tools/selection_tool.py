from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, QAction)
from src.core.base_tool import BaseTool


class SelectionTool(BaseTool):
    def __init__(self):
        super().__init__("Selection", None)

    def create_action(self) -> QAction:
        self._action = QAction(self.name)
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        selection_widget = QWidget()
        layout = QVBoxLayout(selection_widget)

        self.selection_mode_combo = QComboBox()
        self.selection_mode_combo.addItems(["Rectangle", "Ellipse", "Lasso", "Magic Wand"])

        layout.addWidget(QLabel("Selection Mode:"))
        layout.addWidget(self.selection_mode_combo)
        layout.addStretch()

        self._settings_widget = selection_widget
        return selection_widget

    def get_tool_name(self) -> str:
        return "selection"

    def mouse_press_event(self, event, scene, view=None):
        mode = self.selection_mode_combo.currentText()
        pos = event.pos()
        print(f"[SelectionTool] Mouse pressed at ({pos.x()}, {pos.y()}) - Mode: {mode}")

    def mouse_move_event(self, event, scene, view=None):
        pos = event.pos()
        print(f"[SelectionTool] Mouse moved to ({pos.x()}, {pos.y()})")

    def mouse_release_event(self, event, scene, view=None):
        pos = event.pos()
        print(f"[SelectionTool] Mouse released at ({pos.x()}, {pos.y()})")
