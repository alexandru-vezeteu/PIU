from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpinBox,
                             QPushButton, QGroupBox, QComboBox, QAction)
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap
from src.core.base_tool import BaseTool


class ShapeTool(BaseTool):
    def __init__(self, shape_type, color_callback=None, current_color=None):
        names = {
            "rectangle": "Rectangle",
            "circle": "Circle/Ellipse",
            "line": "Line"
        }
        super().__init__(names.get(shape_type, shape_type), None)
        self.shape_type = shape_type
        self.color_callback = color_callback
        self.current_color = current_color
        self.start_pos = None
        self.before_image = None
        self.is_drawing = False

    def create_action(self) -> QAction:
        self._action = QAction(self.name)
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        shape_widget = QWidget()
        layout = QVBoxLayout(shape_widget)

        self.fill_combo = QComboBox()
        self.fill_combo.addItems(["Stroke Only", "Fill Only", "Stroke + Fill"])

        width_label = QLabel("Line Width: 2")
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 50)
        self.width_spin.setValue(2)
        self.width_spin.valueChanged.connect(lambda val: width_label.setText(f"Line Width: {val}"))

        layout.addWidget(QLabel("Draw Mode:"))
        layout.addWidget(self.fill_combo)
        layout.addWidget(width_label)
        layout.addWidget(self.width_spin)
        layout.addStretch()

        self._settings_widget = shape_widget
        return shape_widget

    def get_tool_name(self) -> str:
        return self.shape_type

    def needs_color(self) -> bool:
        return True

    def _draw_shape(self, pixmap: QPixmap, start: QPointF, end: QPointF):
        """Draw the shape on the pixmap."""
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        color = self.current_color if self.current_color else QColor(0, 0, 0)
        line_width = self.width_spin.value()
        mode = self.fill_combo.currentText()
        
        pen = QPen(color)
        pen.setWidth(line_width)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        
        if mode == "Fill Only":
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
        elif mode == "Stroke Only":
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
        else:
            painter.setPen(pen)
            painter.setBrush(QBrush(color))
        
        if self.shape_type == "rectangle":
            rect = QRectF(start, end).normalized()
            painter.drawRect(rect)
        elif self.shape_type == "circle":
            rect = QRectF(start, end).normalized()
            painter.drawEllipse(rect)
        elif self.shape_type == "line":
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawLine(start, end)
        
        painter.end()

    def mouse_press_event(self, event, scene, view=None):
        if view:
            self.start_pos = view.mapToScene(event.pos())
        else:
            self.start_pos = event.pos()
        
        canvas_item = None
        for item in scene.items():
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if canvas_item:
            self.before_image = canvas_item.pixmap().toImage().copy()
            self.is_drawing = True

    def mouse_move_event(self, event, scene, view=None):
        if not self.is_drawing or self.start_pos is None:
            return
        
        if view:
            current_pos = view.mapToScene(event.pos())
        else:
            current_pos = event.pos()
        
        canvas_item = None
        for item in scene.items():
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if not canvas_item or self.before_image is None:
            return
        
        preview_pixmap = QPixmap.fromImage(self.before_image)
        self._draw_shape(preview_pixmap, self.start_pos, current_pos)
        canvas_item.setPixmap(preview_pixmap)

    def mouse_release_event(self, event, scene, view=None):
        from src.commands.pixel_draw_command import PixelDrawCommand
        
        if not self.is_drawing or self.start_pos is None:
            return None
        
        if view:
            end_pos = view.mapToScene(event.pos())
        else:
            end_pos = event.pos()
        
        canvas_item = None
        for item in scene.items():
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if canvas_item and self.before_image is not None:
            final_pixmap = QPixmap.fromImage(self.before_image)
            self._draw_shape(final_pixmap, self.start_pos, end_pos)
            canvas_item.setPixmap(final_pixmap)
            
            after_image = canvas_item.pixmap().toImage().copy()
            
            command = PixelDrawCommand(
                self.before_image,
                after_image,
                f"{self.shape_type.capitalize()} Shape"
            )
            
            self.start_pos = None
            self.before_image = None
            self.is_drawing = False
            
            return command
        
        self.start_pos = None
        self.before_image = None
        self.is_drawing = False
        
        return None
