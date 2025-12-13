from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, QAction,
                             QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPolygonItem,
                             QGraphicsPathItem, QSlider, QGraphicsPixmapItem)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QColor, QBrush, QPolygonF, QPainterPath, QImage, QPixmap, QPainter
from src.core.base_tool import BaseTool
import numpy as np
import cv2


class SelectionTool(BaseTool):
    def __init__(self):
        super().__init__("Selection", None)
        self.start_pos = None
        self.selection_rect = None
        self.selection_item = None
        self.is_selecting = False
        self.lasso_points = []
        self.selection_mask = None
        self.is_moving = False
        self.move_start_pos = None
        self.move_content = None
        self.move_preview_item = None
        self.before_move_image = None

    def create_action(self) -> QAction:
        self._action = QAction(self.name)
        self._action.setCheckable(True)
        return self._action

    def create_settings_panel(self) -> QWidget:
        selection_widget = QWidget()
        layout = QVBoxLayout(selection_widget)

        self.selection_mode_combo = QComboBox()
        self.selection_mode_combo.addItems(["Rectangle", "Ellipse", "Lasso", "Magic Wand"])

        self.tolerance_label = QLabel("Tolerance: 30")
        self.tolerance_slider = QSlider(Qt.Horizontal)
        self.tolerance_slider.setRange(0, 100)
        self.tolerance_slider.setValue(30)
        self.tolerance_slider.valueChanged.connect(lambda val: self.tolerance_label.setText(f"Tolerance: {val}"))

        info_label = QLabel("Click and drag to create a selection.\nMagic Wand: Click to select similar colors.")
        info_label.setWordWrap(True)

        layout.addWidget(QLabel("Selection Mode:"))
        layout.addWidget(self.selection_mode_combo)
        layout.addWidget(self.tolerance_label)
        layout.addWidget(self.tolerance_slider)
        layout.addWidget(info_label)
        layout.addStretch()

        self._settings_widget = selection_widget
        return selection_widget

    def get_tool_name(self) -> str:
        return "selection"

    def _get_pen_and_brush(self):
        pen = QPen(QColor(0, 120, 215))
        pen.setWidth(1)
        pen.setStyle(Qt.DashLine)
        brush = QBrush(QColor(0, 120, 215, 30))
        return pen, brush

    def _create_rect_selection(self, scene, rect):
        if self.selection_item:
            scene.removeItem(self.selection_item)
        self.selection_item = QGraphicsRectItem(rect)
        pen, brush = self._get_pen_and_brush()
        self.selection_item.setPen(pen)
        self.selection_item.setBrush(brush)
        self.selection_item.setZValue(1000)
        self.selection_item.setData(0, 'selection')
        scene.addItem(self.selection_item)

    def _create_ellipse_selection(self, scene, rect):
        if self.selection_item:
            scene.removeItem(self.selection_item)
        self.selection_item = QGraphicsEllipseItem(rect)
        pen, brush = self._get_pen_and_brush()
        self.selection_item.setPen(pen)
        self.selection_item.setBrush(brush)
        self.selection_item.setZValue(1000)
        self.selection_item.setData(0, 'selection')
        scene.addItem(self.selection_item)

    def _create_lasso_selection(self, scene, points):
        if self.selection_item:
            scene.removeItem(self.selection_item)
        if len(points) < 2:
            return
        polygon = QPolygonF([QPointF(p[0], p[1]) for p in points])
        self.selection_item = QGraphicsPolygonItem(polygon)
        pen, brush = self._get_pen_and_brush()
        self.selection_item.setPen(pen)
        self.selection_item.setBrush(brush)
        self.selection_item.setZValue(1000)
        self.selection_item.setData(0, 'selection')
        scene.addItem(self.selection_item)

    def _create_mask_selection(self, scene, mask, canvas_width, canvas_height):
        if self.selection_item:
            scene.removeItem(self.selection_item)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return
        
        path = QPainterPath()
        for contour in contours:
            if len(contour) > 2:
                points = [QPointF(p[0][0], p[0][1]) for p in contour]
                path.addPolygon(QPolygonF(points))
        
        self.selection_item = QGraphicsPathItem(path)
        pen, brush = self._get_pen_and_brush()
        self.selection_item.setPen(pen)
        self.selection_item.setBrush(brush)
        self.selection_item.setZValue(1000)
        self.selection_item.setData(0, 'selection')
        scene.addItem(self.selection_item)

    def clear_selection(self, scene):
        if self.selection_item and self.selection_item.scene():
            scene.removeItem(self.selection_item)
        self.selection_item = None
        self.selection_rect = None
        self.lasso_points = []
        self.selection_mask = None
        print("[Selection] Cleared")

    def get_selection_rect(self):
        return self.selection_rect

    def mouse_press_event(self, event, scene, view=None):
        from PyQt5.QtCore import Qt
        
        mode = self.selection_mode_combo.currentText()
        
        if view:
            click_pos = view.mapToScene(event.pos())
        else:
            click_pos = event.pos()
        
        is_ctrl = event.modifiers() & Qt.ControlModifier
        is_right_click = event.button() == Qt.RightButton
        
        if is_ctrl and is_right_click and self.selection_rect and self.selection_rect.contains(click_pos):
            self._start_move(scene, click_pos)
            return
        
        self.start_pos = click_pos
        
        if self.selection_item:
            scene.removeItem(self.selection_item)
            self.selection_item = None
        
        self.lasso_points = []
        
        if mode == "Magic Wand":
            self._do_magic_wand(scene, int(self.start_pos.x()), int(self.start_pos.y()))
            return
        
        if mode == "Lasso":
            self.lasso_points.append((self.start_pos.x(), self.start_pos.y()))
        
        self.is_selecting = True

    def _start_move(self, scene, click_pos):
        """Start moving the selected content."""
        canvas_item = None
        for item in scene.items():
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if not canvas_item:
            return
        
        canvas_image = canvas_item.pixmap().toImage().copy()
        self.before_move_image = canvas_image.copy()
        
        x = int(self.selection_rect.x())
        y = int(self.selection_rect.y())
        w = int(self.selection_rect.width())
        h = int(self.selection_rect.height())
        
        self.move_content = canvas_image.copy(x, y, w, h)
        
        painter = QPainter(canvas_image)
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(x, y, w, h, Qt.transparent)
        painter.end()
        
        canvas_item.setPixmap(QPixmap.fromImage(canvas_image))
        
        self.move_preview_item = QGraphicsPixmapItem(QPixmap.fromImage(self.move_content))
        self.move_preview_item.setPos(x, y)
        self.move_preview_item.setZValue(999)
        self.move_preview_item.setOpacity(0.8)
        scene.addItem(self.move_preview_item)
        
        self.move_start_pos = click_pos
        self.is_moving = True
        
        print(f"[Selection] Started moving content from ({x}, {y})")

    def mouse_move_event(self, event, scene, view=None):
        if view:
            current_pos = view.mapToScene(event.pos())
        else:
            current_pos = event.pos()
        
        if self.is_moving and self.move_preview_item:
            dx = current_pos.x() - self.move_start_pos.x()
            dy = current_pos.y() - self.move_start_pos.y()
            
            new_x = self.selection_rect.x() + dx
            new_y = self.selection_rect.y() + dy
            
            self.move_preview_item.setPos(new_x, new_y)
            return
        
        if not self.is_selecting or self.start_pos is None:
            return
        
        mode = self.selection_mode_combo.currentText()
        
        if mode == "Rectangle":
            rect = QRectF(self.start_pos, current_pos).normalized()
            self._create_rect_selection(scene, rect)
        elif mode == "Ellipse":
            rect = QRectF(self.start_pos, current_pos).normalized()
            self._create_ellipse_selection(scene, rect)
        elif mode == "Lasso":
            self.lasso_points.append((current_pos.x(), current_pos.y()))
            self._create_lasso_selection(scene, self.lasso_points)

    def mouse_release_event(self, event, scene, view=None):
        if view:
            end_pos = view.mapToScene(event.pos())
        else:
            end_pos = event.pos()
        
        if self.is_moving:
            return self._finish_move(scene, end_pos)
        
        mode = self.selection_mode_combo.currentText()
        
        if mode == "Magic Wand":
            return None
        
        if not self.is_selecting or self.start_pos is None:
            return None
        
        if mode == "Rectangle" or mode == "Ellipse":
            self.selection_rect = QRectF(self.start_pos, end_pos).normalized()
            
            if self.selection_rect.width() > 5 and self.selection_rect.height() > 5:
                if mode == "Rectangle":
                    self._create_rect_selection(scene, self.selection_rect)
                else:
                    self._create_ellipse_selection(scene, self.selection_rect)
                print(f"[Selection] Created {mode.lower()}: ({int(self.selection_rect.x())}, {int(self.selection_rect.y())}) "
                      f"to ({int(self.selection_rect.right())}, {int(self.selection_rect.bottom())})")
            else:
                if self.selection_item:
                    scene.removeItem(self.selection_item)
                    self.selection_item = None
                self.selection_rect = None
        
        elif mode == "Lasso":
            self.lasso_points.append((end_pos.x(), end_pos.y()))
            if len(self.lasso_points) > 2:
                self._create_lasso_selection(scene, self.lasso_points)
                print(f"[Selection] Created lasso with {len(self.lasso_points)} points")
            else:
                if self.selection_item:
                    scene.removeItem(self.selection_item)
                    self.selection_item = None
        
        self.start_pos = None
        self.is_selecting = False
        
        return None

    def _finish_move(self, scene, end_pos):
        """Finish the move operation and return a command."""
        from src.commands.pixel_draw_command import PixelDrawCommand
        
        dx = end_pos.x() - self.move_start_pos.x()
        dy = end_pos.y() - self.move_start_pos.y()
        
        new_x = int(self.selection_rect.x() + dx)
        new_y = int(self.selection_rect.y() + dy)
        
        canvas_item = None
        for item in scene.items():
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if canvas_item and self.move_content:
            current_image = canvas_item.pixmap().toImage()
            
            painter = QPainter(current_image)
            painter.drawImage(new_x, new_y, self.move_content)
            painter.end()
            
            canvas_item.setPixmap(QPixmap.fromImage(current_image))
            
            after_image = current_image.copy()
            command = PixelDrawCommand(self.before_move_image, after_image, "Move Selection")
            
            self.selection_rect = QRectF(new_x, new_y, self.selection_rect.width(), self.selection_rect.height())
            self._create_rect_selection(scene, self.selection_rect)
            
            print(f"[Selection] Moved content to ({new_x}, {new_y})")
        else:
            command = None
        
        if self.move_preview_item:
            scene.removeItem(self.move_preview_item)
            self.move_preview_item = None
        
        self.is_moving = False
        self.move_content = None
        self.before_move_image = None
        self.move_start_pos = None
        
        return command

    def _do_magic_wand(self, scene, x, y):
        canvas_item = None
        for item in scene.items():
            if hasattr(item, 'pixmap') and item.data(0) == 'canvas':
                canvas_item = item
                break
        
        if not canvas_item:
            print("[Magic Wand] No canvas found")
            return
        
        qimage = canvas_item.pixmap().toImage()
        qimage = qimage.convertToFormat(QImage.Format_RGBA8888)
        
        if x < 0 or y < 0 or x >= qimage.width() or y >= qimage.height():
            print("[Magic Wand] Click outside canvas")
            return
        
        ptr = qimage.bits()
        ptr.setsize(qimage.height() * qimage.width() * 4)
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((qimage.height(), qimage.width(), 4)).copy()
        
        rgb = arr[:, :, :3].copy()
        tolerance = self.tolerance_slider.value()
        
        mask = np.zeros((rgb.shape[0] + 2, rgb.shape[1] + 2), np.uint8)
        
        cv2.floodFill(rgb, mask, (x, y), (255, 255, 255),
                      loDiff=(tolerance, tolerance, tolerance),
                      upDiff=(tolerance, tolerance, tolerance),
                      flags=4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8))
        
        self.selection_mask = mask[1:-1, 1:-1]
        
        self._create_mask_selection(scene, self.selection_mask, qimage.width(), qimage.height())
        
        pixel_count = np.count_nonzero(self.selection_mask)
        print(f"[Magic Wand] Selected {pixel_count} pixels at ({x}, {y})")

    def on_tool_deselected(self):
        """Clear selection when switching to another tool."""
        if self.selection_item and self.selection_item.scene():
            self.selection_item.scene().removeItem(self.selection_item)
        self.selection_item = None
        self.selection_rect = None
        self.lasso_points = []
        self.selection_mask = None
