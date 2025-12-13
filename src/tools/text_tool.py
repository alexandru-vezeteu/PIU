from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpinBox,
                             QPushButton, QGroupBox, QComboBox, QAction,
                             QInputDialog, QLineEdit)
from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap
from src.core.base_tool import BaseTool


class TextTool(BaseTool):
    def __init__(self, color_callback=None, current_color=None):
        super().__init__("Text", None)
        self.color_callback = color_callback
        self.current_color = current_color

    def create_action(self) -> QAction:
        self._action = QAction(self.name)
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        text_widget = QWidget()
        layout = QVBoxLayout(text_widget)

        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "Courier New", "Helvetica", "Comic Sans MS"])

        size_label = QLabel("Font Size: 24")
        self.size_spin = QSpinBox()
        self.size_spin.setRange(6, 144)
        self.size_spin.setValue(24)
        self.size_spin.valueChanged.connect(lambda val: size_label.setText(f"Font Size: {val}"))

        layout.addWidget(QLabel("Font:"))
        layout.addWidget(self.font_combo)
        layout.addWidget(size_label)
        layout.addWidget(self.size_spin)
        layout.addStretch()

        self._settings_widget = text_widget
        return text_widget

    def get_tool_name(self) -> str:
        return "text"

    def needs_color(self) -> bool:
        return True

    def mouse_press_event(self, event, scene, view=None):
        from src.commands.pixel_draw_command import PixelDrawCommand
        
        if view:
            scene_pos = view.mapToScene(event.pos())
            parent_widget = view
        else:
            scene_pos = event.pos()
            parent_widget = None
        
        text, ok = QInputDialog.getText(
            parent_widget,
            "Enter Text",
            "Text to add:",
            QLineEdit.Normal,
            ""
        )
        
        if not ok or not text.strip():
            return
        
        canvas_item = None
        for item in scene.items():
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if not canvas_item:
            print("[Text] No canvas found")
            return
        
        before_image = canvas_item.pixmap().toImage().copy()
        
        font_family = self.font_combo.currentText()
        font_size = self.size_spin.value()
        color = self.current_color if self.current_color else QColor(0, 0, 0)
        
        pixmap = canvas_item.pixmap()
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        font = QFont(font_family, font_size)
        painter.setFont(font)
        painter.setPen(color)
        
        painter.drawText(int(scene_pos.x()), int(scene_pos.y()), text)
        
        painter.end()
        canvas_item.setPixmap(pixmap)
        
        after_image = canvas_item.pixmap().toImage().copy()
        
        print(f"[Text] Added '{text}' at ({int(scene_pos.x())}, {int(scene_pos.y())}) - Font: {font_family}, Size: {font_size}")
        
        self._pending_command = PixelDrawCommand(before_image, after_image, "Text")

    def mouse_move_event(self, event, scene, view=None):
        pass

    def mouse_release_event(self, event, scene, view=None):
        if hasattr(self, '_pending_command') and self._pending_command:
            command = self._pending_command
            self._pending_command = None
            return command
        return None
