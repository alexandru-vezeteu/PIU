from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QAction)
from src.core.base_tool import BaseTool


class ZoomTool(BaseTool):
    def __init__(self, image_editor):
        super().__init__("Zoom", icon_path=None)
        self.image_editor = image_editor

    def create_action(self) -> QAction:
        self._action = QAction("Zoom")
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        zoom_widget = QWidget()
        layout = QVBoxLayout(zoom_widget)

        info_label = QLabel("Zoom Controls")
        info_label.setStyleSheet("font-weight: bold;")

        zoom_in_btn = QPushButton("Zoom In (+)")
        zoom_in_btn.clicked.connect(self.image_editor.zoom_in)
        zoom_in_btn.setToolTip("Zoom in by 25% (Ctrl++)")

        zoom_out_btn = QPushButton("Zoom Out (-)")
        zoom_out_btn.clicked.connect(self.image_editor.zoom_out)
        zoom_out_btn.setToolTip("Zoom out by 25% (Ctrl+-)")

        zoom_reset_btn = QPushButton("Reset Zoom (100%)")
        zoom_reset_btn.clicked.connect(self.image_editor.zoom_reset)
        zoom_reset_btn.setToolTip("Reset to 100% (Ctrl+0)")

        zoom_fit_btn = QPushButton("Fit to Window")
        zoom_fit_btn.clicked.connect(self.image_editor.fit_to_window)
        zoom_fit_btn.setToolTip("Fit entire canvas to window (Ctrl+F)")

        tips_label = QLabel("You can also use:\n• Ctrl+Mouse Wheel to zoom\n• Keyboard shortcuts")
        tips_label.setWordWrap(True)
        tips_label.setStyleSheet("color: #666; font-size: 9pt;")

        layout.addWidget(info_label)
        layout.addWidget(zoom_in_btn)
        layout.addWidget(zoom_out_btn)
        layout.addWidget(zoom_reset_btn)
        layout.addWidget(zoom_fit_btn)
        layout.addSpacing(10)
        layout.addWidget(tips_label)
        layout.addStretch()

        self._settings_widget = zoom_widget
        return zoom_widget

    def get_tool_name(self) -> str:
        return "zoom"
    
    def needs_color(self) -> bool:
        return False
