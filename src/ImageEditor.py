from PyQt5.QtWidgets import (QMainWindow, QGraphicsView, QGraphicsScene,
                             QToolBar, QDockWidget, QWidget, QVBoxLayout,
                             QStackedWidget, QAction, QMenu)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QIcon, QColor

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
        self.tool_manager = ToolManager()
        self.filter_manager = FilterManager()

        self.setup_central_widget()
        self.setup_tools()
        self.setup_filters()
        self.setup_ui()
        self.setup_menubar()

        self.tool_manager.select_tool("paintbrush")

    def setup_central_widget(self):
        self.scene = QGraphicsScene()
        self.view = CanvasView(self.scene, self.tool_manager)
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
        file_menu.addAction("New")
        file_menu.addAction("Open...")
        file_menu.addAction("Save")
        file_menu.addAction("Save As...")
        file_menu.addSeparator()
        file_menu.addAction("Exit")

        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cut")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")

        view_menu = menubar.addMenu("View")
        toggle_left_toolbar_action = self.left_toolbar.toggleViewAction()
        toggle_left_toolbar_action.setText("Toggle Tools Panel")
        view_menu.addAction(toggle_left_toolbar_action)

        toggle_right_dock_action = self.right_dock.toggleViewAction()
        toggle_right_dock_action.setText("Toggle Options Panel")
        view_menu.addAction(toggle_right_dock_action)

        toggle_top_toolbar_action = self.top_toolbar.toggleViewAction()
        toggle_top_toolbar_action.setText("Toggle Panel Buttons")
        view_menu.addAction(toggle_top_toolbar_action)

    def on_tool_selected(self, tool):
        tool_name = tool.get_tool_name()
        if tool_name in self.tool_panel_indices:
            self.options_stack.setCurrentIndex(self.tool_panel_indices[tool_name])

        for filter_obj in self.filter_manager.get_filters():
            filter_obj.get_action().setChecked(False)

        self.color_picker_widget.auto_show_for_tool(tool_name)

    def on_filter_selected(self, filter_obj):
        filter_name = filter_obj.get_filter_name()
        if filter_name in self.filter_panel_indices:
            self.options_stack.setCurrentIndex(self.filter_panel_indices[filter_name])

        for tool in self.tool_manager.get_tools():
            tool.get_action().setChecked(False)

    def choose_color(self):
        self.color_picker_widget.choose_color()

    def on_color_changed(self, color):
        self.current_color = color
        for tool in self.tool_manager.get_tools():
            if tool.needs_color() and hasattr(tool, 'update_color_display'):
                tool.update_color_display(color)
