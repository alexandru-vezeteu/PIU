from PyQt5.QtWidgets import (QMainWindow, QGraphicsView, QGraphicsScene,
                             QToolBar, QDockWidget, QWidget, QVBoxLayout,
                             QStackedWidget, QAction, QMenu, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QIcon, QColor, QKeySequence, QPixmap, QImage

from src.core.document import Document
from src.ui.tool_manager import ToolManager
from src.ui.filter_manager import FilterManager
from src.ui.color_picker_widget import ColorPickerWidget
from src.ui.canvas_view import CanvasView

from src.tools.brush_tool import BrushTool
from src.tools.eraser_tool import EraserTool
from src.tools.shape_tool import ShapeTool
from src.tools.text_tool import TextTool
from src.tools.bucket_tool import BucketTool
from src.tools.selection_tool import SelectionTool
from src.tools.color_picker_tool import ColorPickerTool
from src.tools.zoom_tool import ZoomTool

from src.filters.brightness_contrast_filter import BrightnessContrastFilter
from src.filters.blur_filter import BlurFilter
from src.filters.sharpen_filter import SharpenFilter
from src.filters.hue_saturation_filter import HueSaturationFilter
from src.filters.invert_filter import InvertFilter
from src.filters.grayscale_filter import GrayscaleFilter


class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 1200, 800)

        self.current_color = QColor(0, 0, 0)
        self.document = Document()
        self.tool_manager = ToolManager()
        self.filter_manager = FilterManager()

        self.setup_central_widget()
        self.setup_tools()
        self.setup_filters()
        self.setup_ui()
        self.setup_menubar()

        self.tool_manager.select_tool("paintbrush")

    def setup_central_widget(self):
        self.view = CanvasView(self.document, self.tool_manager)
        self.setCentralWidget(self.view)

    def setup_tools(self):
        tools = [
            SelectionTool(),
            BrushTool("paintbrush", self.choose_color, self.current_color),
            BrushTool("airbrush", self.choose_color, self.current_color),
            EraserTool(),
            BucketTool(self.choose_color, self.current_color),
            ShapeTool("rectangle", self.choose_color, self.current_color),
            ShapeTool("circle", self.choose_color, self.current_color),
            ShapeTool("line", self.choose_color, self.current_color),
            TextTool(self.choose_color, self.current_color),
            ColorPickerTool(),
            ZoomTool(self)
        ]

        for tool in tools:
            self.tool_manager.register_tool(tool)

        self.tool_manager.set_tool_selection_callback(self.on_tool_selected)

    def setup_filters(self):
        filters = [
            BrightnessContrastFilter(),
            BlurFilter(),
            SharpenFilter(),
            HueSaturationFilter(),
            InvertFilter(),
            GrayscaleFilter(),
        ]

        for filter_obj in filters:
            self.filter_manager.register_filter(filter_obj)

        self.filter_manager.set_filter_selection_callback(self.on_filter_selected)

    def setup_ui(self):
        self.setup_left_toolbar()
        self.setup_right_dock()
        self.setup_top_toolbar()

    def setup_left_toolbar(self):
        self.left_toolbar = QToolBar("Drawing Tools")
        self.left_toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, self.left_toolbar)

        tools = self.tool_manager.get_tools()

        self.left_toolbar.addAction(tools[0].create_action())
        tools[0].get_action().triggered.connect(lambda: self.tool_manager.select_tool("selection"))

        self.left_toolbar.addSeparator()

        for i in range(1, 5):
            action = tools[i].create_action()
            self.left_toolbar.addAction(action)
            tool = tools[i]
            action.triggered.connect(lambda checked, t=tool: self.tool_manager.select_tool(t.get_tool_name()))

        self.left_toolbar.addSeparator()

        for i in range(5, 8):
            action = tools[i].create_action()
            self.left_toolbar.addAction(action)
            tool = tools[i]
            action.triggered.connect(lambda checked, t=tool: self.tool_manager.select_tool(t.get_tool_name()))

        self.left_toolbar.addSeparator()

        action = tools[8].create_action()
        self.left_toolbar.addAction(action)
        action.triggered.connect(lambda: self.tool_manager.select_tool("text"))

        self.left_toolbar.addSeparator()

        action = tools[9].create_action()
        self.left_toolbar.addAction(action)
        action.triggered.connect(lambda: self.tool_manager.select_tool("color_picker"))

        self.left_toolbar.addSeparator()

        self.filters_toggle_action = QAction("▶ Filters", self)
        self.filters_toggle_action.triggered.connect(self.toggle_filters_menu)
        self.left_toolbar.addAction(self.filters_toggle_action)

        filters = self.filter_manager.get_filters()
        self.filter_actions = []
        for filter_obj in filters:
            action = filter_obj.create_action()
            self.left_toolbar.addAction(action)
            action.setVisible(False)
            action.triggered.connect(
                lambda checked, f=filter_obj: self.filter_manager.select_filter(f.get_filter_name())
            )
            self.filter_actions.append(action)

    def toggle_filters_menu(self):
        expanded = self.filter_manager.toggle_expanded()
        self.filters_toggle_action.setText("▼ Filters" if expanded else "▶ Filters")
        for action in self.filter_actions:
            action.setVisible(expanded)

    def setup_right_dock(self):
        self.right_dock = QDockWidget("Tool Options", self)
        self.right_dock.setAllowedAreas(Qt.RightDockWidgetArea)

        options_widget = QWidget()
        main_layout = QVBoxLayout(options_widget)

        self.options_stack = QStackedWidget()

        self.tool_panel_indices = {}
        for tool in self.tool_manager.get_tools():
            panel = tool.create_settings_panel()
            index = self.options_stack.addWidget(panel)
            self.tool_panel_indices[tool.get_tool_name()] = index

        self.filter_panel_indices = {}
        for filter_obj in self.filter_manager.get_filters():
            panel = filter_obj.create_settings_panel()
            index = self.options_stack.addWidget(panel)
            self.filter_panel_indices[filter_obj.get_filter_name()] = index

        main_layout.addWidget(self.options_stack)
        main_layout.addStretch()

        self.color_picker_widget = ColorPickerWidget(self.current_color)
        self.color_picker_widget.set_color_change_callback(self.on_color_changed)
        main_layout.addWidget(self.color_picker_widget)

        self.right_dock.setWidget(options_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)

    def setup_top_toolbar(self):
        self.top_toolbar = QToolBar("Panel Controls")
        self.addToolBar(Qt.TopToolBarArea, self.top_toolbar)

        self.left_toolbar_button = QAction("Tools Panel", self)
        self.left_toolbar_button.setCheckable(True)
        self.left_toolbar_button.setChecked(True)
        self.left_toolbar_button.triggered.connect(self.toggle_left_toolbar_visibility)
        self.top_toolbar.addAction(self.left_toolbar_button)

        self.right_dock_button = QAction("Options Panel", self)
        self.right_dock_button.setCheckable(True)
        self.right_dock_button.setChecked(True)
        self.right_dock_button.triggered.connect(self.toggle_right_dock_visibility)
        self.top_toolbar.addAction(self.right_dock_button)
        
        self.top_toolbar.addSeparator()
        
        zoom_in_btn = QAction("Zoom +", self)
        zoom_in_btn.triggered.connect(self.zoom_in)
        zoom_in_btn.setToolTip("Zoom In (Ctrl++)")
        self.top_toolbar.addAction(zoom_in_btn)
        
        zoom_out_btn = QAction("Zoom -", self)
        zoom_out_btn.triggered.connect(self.zoom_out)
        zoom_out_btn.setToolTip("Zoom Out (Ctrl+-)")
        self.top_toolbar.addAction(zoom_out_btn)
        
        zoom_fit_btn = QAction("Fit", self)
        zoom_fit_btn.triggered.connect(self.fit_to_window)
        zoom_fit_btn.setToolTip("Fit to Window (Ctrl+F)")
        self.top_toolbar.addAction(zoom_fit_btn)

        self.left_toolbar.visibilityChanged.connect(self.sync_left_toolbar_button)
        self.right_dock.visibilityChanged.connect(self.sync_right_dock_button)

    def toggle_left_toolbar_visibility(self):
        self.left_toolbar.setVisible(not self.left_toolbar.isVisible())

    def toggle_right_dock_visibility(self):
        self.right_dock.setVisible(not self.right_dock.isVisible())

    def sync_left_toolbar_button(self, visible):
        self.left_toolbar_button.setChecked(visible)

    def sync_right_dock_button(self, visible):
        self.right_dock_button.setChecked(visible)

    def setup_menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_document)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_document)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_document)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_document_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("Edit")
        
        self.undo_action = QAction("Undo", self)
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.undo_action.triggered.connect(self.perform_undo)
        edit_menu.addAction(self.undo_action)
        
        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut(QKeySequence.Redo) 
        self.redo_action.triggered.connect(self.perform_redo)
        edit_menu.addAction(self.redo_action)
        
        edit_menu.addSeparator()
        edit_menu.addAction("Cut")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")
        
        self.update_undo_redo_states()

        view_menu = menubar.addMenu("View")
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence.ZoomIn)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence.ZoomOut)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        zoom_reset_action = QAction("Reset Zoom", self)
        zoom_reset_action.setShortcut("Ctrl+0")
        zoom_reset_action.triggered.connect(self.zoom_reset)
        view_menu.addAction(zoom_reset_action)
        
        fit_to_window_action = QAction("Fit to Window", self)
        fit_to_window_action.setShortcut("Ctrl+F")
        fit_to_window_action.triggered.connect(self.fit_to_window)
        view_menu.addAction(fit_to_window_action)
        
        view_menu.addSeparator()
        
        toggle_left_toolbar_action = self.left_toolbar.toggleViewAction()
        toggle_left_toolbar_action.setText("Toggle Tools Panel")
        view_menu.addAction(toggle_left_toolbar_action)

        toggle_right_dock_action = self.right_dock.toggleViewAction()
        toggle_right_dock_action.setText("Toggle Options Panel")
        view_menu.addAction(toggle_right_dock_action)

        toggle_top_toolbar_action = self.top_toolbar.toggleViewAction()
        toggle_top_toolbar_action.setText("Toggle Panel Buttons")
        view_menu.addAction(toggle_top_toolbar_action)
    
    def perform_undo(self):
        """Perform undo operation."""
        if self.document.undo():
            self.update_undo_redo_states()
            self.view.viewport().update()
    
    def perform_redo(self):
        """Perform redo operation."""
        if self.document.redo():
            self.update_undo_redo_states()
            self.view.viewport().update()
    
    def update_undo_redo_states(self):
        """Update undo/redo menu item states and text."""
        if self.document.can_undo():
            self.undo_action.setEnabled(True)
            undo_name = self.document.get_undo_name()
            self.undo_action.setText(f"Undo {undo_name}" if undo_name else "Undo")
        else:
            self.undo_action.setEnabled(False)
            self.undo_action.setText("Undo")
        
        if self.document.can_redo():
            self.redo_action.setEnabled(True)
            redo_name = self.document.get_redo_name()
            self.redo_action.setText(f"Redo {redo_name}" if redo_name else "Redo")
        else:
            self.redo_action.setEnabled(False)
            self.redo_action.setText("Redo")

    def on_tool_selected(self, tool):
        tool_name = tool.get_tool_name()
        if tool_name in self.tool_panel_indices:
            self.options_stack.setCurrentIndex(self.tool_panel_indices[tool_name])

        for filter_obj in self.filter_manager.get_filters():
            filter_obj.get_action().setChecked(False)

        self.color_picker_widget.auto_show_for_tool(tool_name)

    def on_filter_selected(self, filter_obj):
        filter_name = filter_obj.get_filter_name()
        print(f"[Filter] Selected: {filter_name}")
        
        settings_widget = filter_obj.get_settings_widget()
        if settings_widget:
            self.options_stack.addWidget(settings_widget)
            self.options_stack.setCurrentWidget(settings_widget)
        
        if filter_name == "invert" and hasattr(filter_obj, 'apply_btn'):
            try:
                filter_obj.apply_btn.clicked.disconnect()
            except:
                pass
            filter_obj.apply_btn.clicked.connect(lambda: self.apply_filter_to_canvas(filter_obj))
            print(f"[Filter] Connected {filter_name} apply button")

    def choose_color(self):
        self.color_picker_widget.choose_color()

    def on_color_changed(self, color):
        self.current_color = color
        for tool in self.tool_manager.get_tools():
            if tool.needs_color() and hasattr(tool, 'update_color_display'):
                tool.update_color_display(color)
    
    def apply_filter_to_canvas(self, filter_obj):
        """Apply a filter to the canvas with undo/redo support."""
        from src.commands.filter_command import FilterCommand
        
        print(f"[Filter] Applying {filter_obj.name} filter...")
        
        command = FilterCommand(
            self.document.scene,
            filter_obj.apply_filter,
            filter_obj.name
        )
        
        print(f"[Filter] FilterCommand created, executing...")
        
        self.document.execute_command(command)
        self.update_undo_redo_states()
        self.view.viewport().update()
        
        print(f"[Filter] {filter_obj.name} filter applied successfully!")
    
    def new_document(self):
        """Create a new blank document."""
        reply = QMessageBox.question(self, 'New Document',
                                    'Create a new document? Unsaved changes will be lost.',
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.document.scene.clear()
            self.document.clear_history()
            self.update_undo_redo_states()
            self.view.viewport().update()
    
    def open_document(self):
        """Open an image file."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        
        if filename:
            pixmap = QPixmap(filename)
            if not pixmap.isNull():
                self.document.scene.clear()
                
                self.document.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
                self.document.width = pixmap.width()
                self.document.height = pixmap.height()
                
                self.document.scene.addPixmap(pixmap)
                
                self.view.setSceneRect(self.document.scene.sceneRect())
                
                self.fit_to_window()
                
                self.document.clear_history()
                self.update_undo_redo_states()
                self.view.viewport().update()
            else:
                QMessageBox.warning(self, "Error", "Failed to load image.")
    
    def save_document(self):
        """Save the document (if no filename, prompt for one)."""
        if hasattr(self, 'current_filename') and self.current_filename:
            self._save_to_file(self.current_filename)
        else:
            self.save_document_as()
    
    def save_document_as(self):
        """Save the document with a new filename."""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "PNG Image (*.png);;JPEG Image (*.jpg);;All Files (*)"
        )
        
        if filename:
            self._save_to_file(filename)
            self.current_filename = filename
    
    def _save_to_file(self, filename):
        """Save the scene to an image file."""
        rect = self.document.scene.sceneRect()
        image = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB32)
        image.fill(0xFFFFFFFF)
        
        painter = QPainter(image)
        self.document.scene.render(painter)
        painter.end()
        
        if image.save(filename):
            QMessageBox.information(self, "Success", f"Image saved to {filename}")
        else:
            QMessageBox.warning(self, "Error", "Failed to save image.")
    
    def zoom_in(self):
        """Zoom in by 25%."""
        self.view.scale(1.25, 1.25)
    
    def zoom_out(self):
        """Zoom out by 25%."""
        self.view.scale(0.8, 0.8)
    
    def zoom_reset(self):
        """Reset zoom to 100%."""
        self.view.resetTransform()
    
    def fit_to_window(self):
        """Fit the entire scene to the window."""
        self.view.fitInView(self.document.scene.sceneRect(), Qt.KeepAspectRatio)
