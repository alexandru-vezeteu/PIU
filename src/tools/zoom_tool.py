from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QAction, QLabel
from PyQt5.QtCore import Qt
from src.core.base_tool import BaseTool


class ZoomTool(BaseTool):
    def __init__(self, editor):
        super().__init__("Zoom", icon_path=None)
        self.editor = editor
        
    def create_action(self) -> QAction:
        self._action = QAction(self.name)
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        zoom_widget = QWidget()
        layout = QVBoxLayout(zoom_widget)
        
        info_label = QLabel("Zoom Controls")
        info_label.setStyleSheet("font-weight: bold;")
        
        zoom_in_btn = QPushButton("Zoom In (+)")
        zoom_in_btn.clicked.connect(self.editor.zoom_in)
        zoom_in_btn.setToolTip("Zoom in (Ctrl++)")
        
        zoom_out_btn = QPushButton("Zoom Out (-)")
        zoom_out_btn.clicked.connect(self.editor.zoom_out)
        zoom_out_btn.setToolTip("Zoom out (Ctrl+-)")
        
        reset_btn = QPushButton("Reset (100%)")
        reset_btn.clicked.connect(self.editor.zoom_reset)
        reset_btn.setToolTip("Reset to 100% (Ctrl+0)")
        
        fit_btn = QPushButton("Fit to Window")
        fit_btn.clicked.connect(self.editor.fit_to_window)
        fit_btn.setToolTip("Fit entire canvas (Ctrl+F)")
        
        tips_label = QLabel("Tip: Use Ctrl+Mouse Wheel to zoom")
        tips_label.setWordWrap(True)
        tips_label.setStyleSheet("color: #666; font-size: 9pt;")
        
        layout.addWidget(info_label)
        layout.addWidget(zoom_in_btn)
        layout.addWidget(zoom_out_btn)
        layout.addWidget(reset_btn)
        layout.addWidget(fit_btn)
        layout.addSpacing(10)
        layout.addWidget(tips_label)
        layout.addStretch()
        
        self._settings_widget = zoom_widget
        return zoom_widget

    def get_tool_name(self) -> str:
        return "zoom"
    
    def register_bindings(self, bind_func):
        """Register Ctrl+Scroll for zoom."""
        print("[ZoomTool] Registering Ctrl+Scroll zoom binding")
        pass
