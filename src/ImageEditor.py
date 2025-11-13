from PyQt5.QtWidgets import (
    QMainWindow, QGraphicsView, QGraphicsScene, QToolBar,
    QAction, QDockWidget, QWidget, QVBoxLayout, QLabel, QSlider,
    QColorDialog, QPushButton, QSpinBox, QComboBox, QGroupBox, QStackedWidget,
    QWidgetAction, QFrame, QHBoxLayout, QGridLayout
    )
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QIcon, QColor
class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 1200, 800)

        self.current_tool = "paintbrush"
        self.current_color = QColor(0, 0, 0)  # Default to black

        self.color_palette = [
            QColor(0, 0, 0),      # Black
            QColor(255, 255, 255), # White
            QColor(255, 0, 0),     # Red
            QColor(0, 255, 0),     # Green
            QColor(0, 0, 255),     # Blue
            QColor(255, 255, 0),   # Yellow
            QColor(255, 0, 255),   # Magenta
            QColor(0, 255, 255),   # Cyan
        ]
        self.recent_colors = []  # Will store recently used colors

        self.setup_ui()

    def setup_ui(self):
        self.setup_central_widget()
        self.setup_left_toolbar()
        self.setup_right_dock()
        self.setup_toggle_buttons()
        self.setup_menu_bar()
        self.left_toolbar_visible = True
        self.right_dock_visible = True

    def setup_central_widget(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)

    def select_tool(self, tool_name):
        """Handle tool selection and update UI"""
        self.current_tool = tool_name

        for name, action in self.tool_actions.items():
            action.setChecked(name == tool_name)

        self.update_right_panel_for_tool(tool_name)

        self.auto_show_hide_color_picker(tool_name)

    def toggle_left_toolbar_visibility(self):
        self.left_toolbar_visible = not self.left_toolbar_visible
        self.left_toolbar.setVisible(self.left_toolbar_visible)
        
    def setup_left_toolbar(self):

        self.left_toolbar = QToolBar("Drawing Tools")
        self.left_toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, self.left_toolbar)

        action_selection = QAction(QIcon(), "Selection", self)
        action_selection.setCheckable(True)
        action_selection.triggered.connect(lambda: self.select_tool("selection"))

        action_paintbrush = QAction(QIcon("assets/icons/paint_brush.png"), "Paintbrush", self)
        action_paintbrush.setCheckable(True)
        action_paintbrush.setChecked(True)  # Default tool
        action_paintbrush.triggered.connect(lambda: self.select_tool("paintbrush"))

        action_airbrush = QAction(QIcon(), "Airbrush", self)
        action_airbrush.setCheckable(True)
        action_airbrush.triggered.connect(lambda: self.select_tool("airbrush"))

        action_eraser = QAction(QIcon(), "Eraser", self)
        action_eraser.setCheckable(True)
        action_eraser.triggered.connect(lambda: self.select_tool("eraser"))

        action_paint_bucket = QAction(QIcon(), "Paint Bucket", self)
        action_paint_bucket.setCheckable(True)
        action_paint_bucket.triggered.connect(lambda: self.select_tool("paint_bucket"))

        action_rectangle = QAction(QIcon(), "Rectangle", self)
        action_rectangle.setCheckable(True)
        action_rectangle.triggered.connect(lambda: self.select_tool("rectangle"))

        action_circle = QAction(QIcon(), "Circle/Ellipse", self)
        action_circle.setCheckable(True)
        action_circle.triggered.connect(lambda: self.select_tool("circle"))

        action_line = QAction(QIcon(), "Line", self)
        action_line.setCheckable(True)
        action_line.triggered.connect(lambda: self.select_tool("line"))

        action_text = QAction(QIcon(), "Text", self)
        action_text.setCheckable(True)
        action_text.triggered.connect(lambda: self.select_tool("text"))

        action_color_picker = QAction(QIcon(), "Eyedropper", self)
        action_color_picker.setCheckable(True)
        action_color_picker.triggered.connect(lambda: self.select_tool("color_picker"))

        self.tool_actions = {
            "selection": action_selection,
            "paintbrush": action_paintbrush,
            "airbrush": action_airbrush,
            "eraser": action_eraser,
            "paint_bucket": action_paint_bucket,
            "rectangle": action_rectangle,
            "circle": action_circle,
            "line": action_line,
            "text": action_text,
            "color_picker": action_color_picker
        }

        self.left_toolbar.addAction(action_selection)
        self.left_toolbar.addSeparator()
        self.left_toolbar.addAction(action_paintbrush)
        self.left_toolbar.addAction(action_airbrush)
        self.left_toolbar.addAction(action_eraser)
        self.left_toolbar.addAction(action_paint_bucket)
        self.left_toolbar.addSeparator()
        self.left_toolbar.addAction(action_rectangle)
        self.left_toolbar.addAction(action_circle)
        self.left_toolbar.addAction(action_line)
        self.left_toolbar.addSeparator()
        self.left_toolbar.addAction(action_text)
        self.left_toolbar.addSeparator()
        self.left_toolbar.addAction(action_color_picker)
        self.left_toolbar.addSeparator()

        self.setup_filters_section()
    def setup_filters_section(self):
        """Create a collapsible filters section in the left toolbar"""
        self.filters_expanded = False
        action_filters_toggle = QAction(QIcon(), "▶ Filters", self)
        action_filters_toggle.triggered.connect(self.toggle_filters_menu)
        self.filters_toggle_action = action_filters_toggle
        self.left_toolbar.addAction(action_filters_toggle)

        self.filter_actions_list = []

        action_brightness_contrast = QAction(QIcon(), "  Brightness/Contrast", self)
        action_brightness_contrast.setCheckable(True)
        action_brightness_contrast.triggered.connect(lambda: self.select_filter("brightness_contrast"))
        self.filter_actions_list.append(action_brightness_contrast)

        action_blur = QAction(QIcon(), "  Blur", self)
        action_blur.setCheckable(True)
        action_blur.triggered.connect(lambda: self.select_filter("blur"))
        self.filter_actions_list.append(action_blur)

        action_sharpen = QAction(QIcon(), "  Sharpen", self)
        action_sharpen.setCheckable(True)
        action_sharpen.triggered.connect(lambda: self.select_filter("sharpen"))
        self.filter_actions_list.append(action_sharpen)

        action_hue_saturation = QAction(QIcon(), "  Hue/Saturation", self)
        action_hue_saturation.setCheckable(True)
        action_hue_saturation.triggered.connect(lambda: self.select_filter("hue_saturation"))
        self.filter_actions_list.append(action_hue_saturation)

        action_invert = QAction(QIcon(), "  Invert Colors", self)
        action_invert.setCheckable(True)
        action_invert.triggered.connect(lambda: self.select_filter("invert"))
        self.filter_actions_list.append(action_invert)

        action_grayscale = QAction(QIcon(), "  Grayscale", self)
        action_grayscale.setCheckable(True)
        action_grayscale.triggered.connect(lambda: self.select_filter("grayscale"))
        self.filter_actions_list.append(action_grayscale)

        self.filter_tool_actions = {
            "brightness_contrast": action_brightness_contrast,
            "blur": action_blur,
            "sharpen": action_sharpen,
            "hue_saturation": action_hue_saturation,
            "invert": action_invert,
            "grayscale": action_grayscale
        }

        for action in self.filter_actions_list:
            self.left_toolbar.addAction(action)
            action.setVisible(False)  # Start hidden

    def toggle_filters_menu(self):
        """Toggle the visibility of filter options"""
        self.filters_expanded = not self.filters_expanded

        if self.filters_expanded:
            self.filters_toggle_action.setText("▼ Filters")
        else:
            self.filters_toggle_action.setText("▶ Filters")

        for action in self.filter_actions_list:
            action.setVisible(self.filters_expanded)

    def select_filter(self, filter_name):
        """Handle filter selection and update UI"""
        self.current_tool = f"filter_{filter_name}"

        for name, action in self.tool_actions.items():
            action.setChecked(False)

        for name, action in self.filter_tool_actions.items():
            action.setChecked(name == filter_name)

        self.update_right_panel_for_filter(filter_name)

    def toggle_right_dock_visibility(self):
        self.right_dock_visible = not self.right_dock_visible
        self.right_dock.setVisible(self.right_dock_visible)
        
    def setup_right_dock(self):
        self.right_dock = QDockWidget("Tool Options", self)
        self.right_dock.setAllowedAreas(Qt.RightDockWidgetArea)

        options_widget = QWidget()
        main_layout = QVBoxLayout(options_widget)

        self.options_stack = QStackedWidget()

        self.create_brush_settings()
        self.create_eraser_settings()
        self.create_shape_settings()
        self.create_text_settings()
        self.create_bucket_settings()
        self.create_selection_settings()

        self.create_brightness_contrast_settings()
        self.create_blur_settings()
        self.create_sharpen_settings()
        self.create_hue_saturation_settings()
        self.create_invert_settings()
        self.create_grayscale_settings()

        self.create_color_picker_panel()

        main_layout.addWidget(self.options_stack)
        main_layout.addStretch()

        self.add_bottom_color_picker(main_layout)

        self.right_dock.setWidget(options_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)

    def create_brush_settings(self):
        """Settings for Paintbrush and Airbrush tools"""
        brush_widget = QWidget()
        layout = QVBoxLayout(brush_widget)

        color_group = QGroupBox("Color")
        color_layout = QVBoxLayout()
        self.brush_color_button = QPushButton()
        self.brush_color_button.setFixedSize(100, 30)
        self.brush_color_button.setStyleSheet(f"QPushButton {{ background-color: {self.current_color.name()}; border: 2px solid #666; }}")
        self.brush_color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(QLabel("Current Color:"))
        color_layout.addWidget(self.brush_color_button)
        color_group.setLayout(color_layout)

        size_label = QLabel("Brush Size: 5")
        self.brush_size_spin = QSpinBox()
        self.brush_size_spin.setRange(1, 100)
        self.brush_size_spin.setValue(5)
        self.brush_size_spin.valueChanged.connect(lambda val: size_label.setText(f"Brush Size: {val}"))

        opacity_label = QLabel("Opacity: 100%")
        self.brush_opacity_slider = QSlider(Qt.Horizontal)
        self.brush_opacity_slider.setRange(0, 100)
        self.brush_opacity_slider.setValue(100)
        self.brush_opacity_slider.valueChanged.connect(lambda val: opacity_label.setText(f"Opacity: {val}%"))

        hardness_label = QLabel("Hardness: 100%")
        self.brush_hardness_slider = QSlider(Qt.Horizontal)
        self.brush_hardness_slider.setRange(0, 100)
        self.brush_hardness_slider.setValue(100)
        self.brush_hardness_slider.valueChanged.connect(lambda val: hardness_label.setText(f"Hardness: {val}%"))

        layout.addWidget(color_group)
        layout.addWidget(QLabel("Size:"))
        layout.addWidget(size_label)
        layout.addWidget(self.brush_size_spin)
        layout.addWidget(opacity_label)
        layout.addWidget(self.brush_opacity_slider)
        layout.addWidget(hardness_label)
        layout.addWidget(self.brush_hardness_slider)
        layout.addStretch()

        self.brush_settings_index = self.options_stack.addWidget(brush_widget)

    def create_eraser_settings(self):
        """Settings for Eraser tool"""
        eraser_widget = QWidget()
        layout = QVBoxLayout(eraser_widget)

        size_label = QLabel("Eraser Size: 10")
        self.eraser_size_spin = QSpinBox()
        self.eraser_size_spin.setRange(1, 100)
        self.eraser_size_spin.setValue(10)
        self.eraser_size_spin.valueChanged.connect(lambda val: size_label.setText(f"Eraser Size: {val}"))

        hardness_label = QLabel("Hardness: 100%")
        self.eraser_hardness_slider = QSlider(Qt.Horizontal)
        self.eraser_hardness_slider.setRange(0, 100)
        self.eraser_hardness_slider.setValue(100)
        self.eraser_hardness_slider.valueChanged.connect(lambda val: hardness_label.setText(f"Hardness: {val}%"))

        layout.addWidget(QLabel("Size:"))
        layout.addWidget(size_label)
        layout.addWidget(self.eraser_size_spin)
        layout.addWidget(hardness_label)
        layout.addWidget(self.eraser_hardness_slider)
        layout.addStretch()

        self.eraser_settings_index = self.options_stack.addWidget(eraser_widget)

    def create_shape_settings(self):
        """Settings for Shape tools (Rectangle, Circle, Line)"""
        shape_widget = QWidget()
        layout = QVBoxLayout(shape_widget)

        color_group = QGroupBox("Color")
        color_layout = QVBoxLayout()
        self.shape_color_button = QPushButton()
        self.shape_color_button.setFixedSize(100, 30)
        self.shape_color_button.setStyleSheet(f"QPushButton {{ background-color: {self.current_color.name()}; border: 2px solid #666; }}")
        self.shape_color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(QLabel("Stroke Color:"))
        color_layout.addWidget(self.shape_color_button)
        color_group.setLayout(color_layout)

        self.shape_fill_combo = QComboBox()
        self.shape_fill_combo.addItems(["Stroke Only", "Fill Only", "Stroke + Fill"])

        width_label = QLabel("Line Width: 2")
        self.shape_width_spin = QSpinBox()
        self.shape_width_spin.setRange(1, 50)
        self.shape_width_spin.setValue(2)
        self.shape_width_spin.valueChanged.connect(lambda val: width_label.setText(f"Line Width: {val}"))

        layout.addWidget(color_group)
        layout.addWidget(QLabel("Draw Mode:"))
        layout.addWidget(self.shape_fill_combo)
        layout.addWidget(width_label)
        layout.addWidget(self.shape_width_spin)
        layout.addStretch()

        self.shape_settings_index = self.options_stack.addWidget(shape_widget)

    def create_text_settings(self):
        """Settings for Text tool"""
        text_widget = QWidget()
        layout = QVBoxLayout(text_widget)

        self.text_font_combo = QComboBox()
        self.text_font_combo.addItems(["Arial", "Times New Roman", "Courier New", "Helvetica", "Comic Sans MS"])

        size_label = QLabel("Font Size: 12")
        self.text_size_spin = QSpinBox()
        self.text_size_spin.setRange(6, 144)
        self.text_size_spin.setValue(12)
        self.text_size_spin.valueChanged.connect(lambda val: size_label.setText(f"Font Size: {val}"))

        color_group = QGroupBox("Color")
        color_layout = QVBoxLayout()
        self.text_color_button = QPushButton()
        self.text_color_button.setFixedSize(100, 30)
        self.text_color_button.setStyleSheet(f"QPushButton {{ background-color: {self.current_color.name()}; border: 2px solid #666; }}")
        self.text_color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(QLabel("Text Color:"))
        color_layout.addWidget(self.text_color_button)
        color_group.setLayout(color_layout)

        layout.addWidget(QLabel("Font:"))
        layout.addWidget(self.text_font_combo)
        layout.addWidget(size_label)
        layout.addWidget(self.text_size_spin)
        layout.addWidget(color_group)
        layout.addStretch()

        self.text_settings_index = self.options_stack.addWidget(text_widget)

    def create_bucket_settings(self):
        """Settings for Paint Bucket tool"""
        bucket_widget = QWidget()
        layout = QVBoxLayout(bucket_widget)

        color_group = QGroupBox("Color")
        color_layout = QVBoxLayout()
        self.bucket_color_button = QPushButton()
        self.bucket_color_button.setFixedSize(100, 30)
        self.bucket_color_button.setStyleSheet(f"QPushButton {{ background-color: {self.current_color.name()}; border: 2px solid #666; }}")
        self.bucket_color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(QLabel("Fill Color:"))
        color_layout.addWidget(self.bucket_color_button)
        color_group.setLayout(color_layout)

        tolerance_label = QLabel("Tolerance: 30")
        self.bucket_tolerance_slider = QSlider(Qt.Horizontal)
        self.bucket_tolerance_slider.setRange(0, 100)
        self.bucket_tolerance_slider.setValue(30)
        self.bucket_tolerance_slider.valueChanged.connect(lambda val: tolerance_label.setText(f"Tolerance: {val}"))

        layout.addWidget(color_group)
        layout.addWidget(tolerance_label)
        layout.addWidget(self.bucket_tolerance_slider)
        layout.addStretch()

        self.bucket_settings_index = self.options_stack.addWidget(bucket_widget)

    def create_selection_settings(self):
        """Settings for Selection tool"""
        selection_widget = QWidget()
        layout = QVBoxLayout(selection_widget)

        info_label = QLabel("Click and drag to select an area.\nUse Edit menu for copy/paste/delete.")
        info_label.setWordWrap(True)

        layout.addWidget(info_label)
        layout.addStretch()

        self.selection_settings_index = self.options_stack.addWidget(selection_widget)

    def create_brightness_contrast_settings(self):
        """Settings for Brightness/Contrast filter"""
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        self.brightness_label = QLabel("Brightness: 0")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(lambda val: self.brightness_label.setText(f"Brightness: {val}"))

        self.contrast_label = QLabel("Contrast: 0")
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(-100, 100)
        self.contrast_slider.setValue(0)
        self.contrast_slider.valueChanged.connect(lambda val: self.contrast_label.setText(f"Contrast: {val}"))

        apply_btn = QPushButton("Apply Filter")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(lambda: (self.brightness_slider.setValue(0), self.contrast_slider.setValue(0)))

        layout.addWidget(QLabel("Brightness:"))
        layout.addWidget(self.brightness_label)
        layout.addWidget(self.brightness_slider)
        layout.addWidget(QLabel("Contrast:"))
        layout.addWidget(self.contrast_label)
        layout.addWidget(self.contrast_slider)
        layout.addWidget(apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self.brightness_contrast_settings_index = self.options_stack.addWidget(filter_widget)

    def create_blur_settings(self):
        """Settings for Blur filter"""
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        blur_type_label = QLabel("Blur Type:")
        self.blur_type_combo = QComboBox()
        self.blur_type_combo.addItems(["Gaussian Blur", "Motion Blur", "Box Blur"])

        radius_label = QLabel("Radius: 5")
        self.blur_radius_slider = QSlider(Qt.Horizontal)
        self.blur_radius_slider.setRange(1, 50)
        self.blur_radius_slider.setValue(5)
        self.blur_radius_slider.valueChanged.connect(lambda val: radius_label.setText(f"Radius: {val}"))

        apply_btn = QPushButton("Apply Filter")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(lambda: self.blur_radius_slider.setValue(5))

        layout.addWidget(blur_type_label)
        layout.addWidget(self.blur_type_combo)
        layout.addWidget(radius_label)
        layout.addWidget(self.blur_radius_slider)
        layout.addWidget(apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self.blur_settings_index = self.options_stack.addWidget(filter_widget)

    def create_sharpen_settings(self):
        """Settings for Sharpen filter"""
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        amount_label = QLabel("Amount: 50%")
        self.sharpen_amount_slider = QSlider(Qt.Horizontal)
        self.sharpen_amount_slider.setRange(0, 100)
        self.sharpen_amount_slider.setValue(50)
        self.sharpen_amount_slider.valueChanged.connect(lambda val: amount_label.setText(f"Amount: {val}%"))

        apply_btn = QPushButton("Apply Filter")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(lambda: self.sharpen_amount_slider.setValue(50))

        layout.addWidget(amount_label)
        layout.addWidget(self.sharpen_amount_slider)
        layout.addWidget(apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self.sharpen_settings_index = self.options_stack.addWidget(filter_widget)

    def create_hue_saturation_settings(self):
        """Settings for Hue/Saturation filter"""
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        hue_label = QLabel("Hue: 0")
        self.hue_slider = QSlider(Qt.Horizontal)
        self.hue_slider.setRange(-180, 180)
        self.hue_slider.setValue(0)
        self.hue_slider.valueChanged.connect(lambda val: hue_label.setText(f"Hue: {val}"))

        saturation_label = QLabel("Saturation: 0")
        self.saturation_slider = QSlider(Qt.Horizontal)
        self.saturation_slider.setRange(-100, 100)
        self.saturation_slider.setValue(0)
        self.saturation_slider.valueChanged.connect(lambda val: saturation_label.setText(f"Saturation: {val}"))

        lightness_label = QLabel("Lightness: 0")
        self.lightness_slider = QSlider(Qt.Horizontal)
        self.lightness_slider.setRange(-100, 100)
        self.lightness_slider.setValue(0)
        self.lightness_slider.valueChanged.connect(lambda val: lightness_label.setText(f"Lightness: {val}"))

        apply_btn = QPushButton("Apply Filter")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(lambda: (self.hue_slider.setValue(0), self.saturation_slider.setValue(0), self.lightness_slider.setValue(0)))

        layout.addWidget(hue_label)
        layout.addWidget(self.hue_slider)
        layout.addWidget(saturation_label)
        layout.addWidget(self.saturation_slider)
        layout.addWidget(lightness_label)
        layout.addWidget(self.lightness_slider)
        layout.addWidget(apply_btn)
        layout.addWidget(reset_btn)
        layout.addStretch()

        self.hue_saturation_settings_index = self.options_stack.addWidget(filter_widget)

    def create_invert_settings(self):
        """Settings for Invert Colors filter"""
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        info_label = QLabel("This filter inverts all colors in the image.\nNo additional settings required.")
        info_label.setWordWrap(True)

        apply_btn = QPushButton("Apply Filter")

        layout.addWidget(info_label)
        layout.addWidget(apply_btn)
        layout.addStretch()

        self.invert_settings_index = self.options_stack.addWidget(filter_widget)

    def create_grayscale_settings(self):
        """Settings for Grayscale filter"""
        filter_widget = QWidget()
        layout = QVBoxLayout(filter_widget)

        info_label = QLabel("Converts the image to grayscale.\nNo additional settings required.")
        info_label.setWordWrap(True)

        apply_btn = QPushButton("Apply Filter")

        layout.addWidget(info_label)
        layout.addWidget(apply_btn)
        layout.addStretch()

        self.grayscale_settings_index = self.options_stack.addWidget(filter_widget)

    def create_color_picker_panel(self):
        """Settings for Color Picker tool (Eyedropper)"""
        picker_widget = QWidget()
        layout = QVBoxLayout(picker_widget)

        info_label = QLabel("Click on the canvas to pick a color from the image.")
        info_label.setWordWrap(True)

        layout.addWidget(info_label)
        layout.addStretch()

        self.color_picker_settings_index = self.options_stack.addWidget(picker_widget)

    def add_bottom_color_picker(self, parent_layout):
        """Add a persistent color picker section at the bottom of the right panel"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        parent_layout.addWidget(separator)

        self.color_section = QGroupBox("Color Picker")
        color_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        toggle_color_btn = QPushButton("▼ Hide")
        toggle_color_btn.setFixedWidth(80)
        toggle_color_btn.setStyleSheet("QPushButton { background-color: transparent; border: none; text-align: left; }")
        toggle_color_btn.clicked.connect(self.toggle_color_picker_visibility)
        self.color_picker_toggle_btn = toggle_color_btn

        header_layout.addWidget(QLabel("<b>Color Picker</b>"))
        header_layout.addStretch()
        header_layout.addWidget(toggle_color_btn)

        color_layout.addLayout(header_layout)

        self.color_picker_content = QWidget()
        content_layout = QVBoxLayout(self.color_picker_content)

        current_color_layout = QHBoxLayout()
        current_color_layout.addWidget(QLabel("Current Color:"))

        self.main_color_button = QPushButton()
        self.main_color_button.setFixedSize(80, 40)
        self.main_color_button.setStyleSheet(f"QPushButton {{ background-color: {self.current_color.name()}; border: 2px solid #666; }}")
        self.main_color_button.clicked.connect(self.choose_color)
        self.main_color_button.setToolTip("Click to choose a custom color")
        current_color_layout.addWidget(self.main_color_button)
        current_color_layout.addStretch()

        content_layout.addLayout(current_color_layout)

        palette_label = QLabel("Preset Colors:")
        content_layout.addWidget(palette_label)

        palette_grid = QGridLayout()
        palette_grid.setSpacing(2)

        self.palette_buttons = []
        for i, color in enumerate(self.color_palette):
            btn = QPushButton()
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(f"QPushButton {{ background-color: {color.name()}; border: 1px solid #333; }} QPushButton:hover {{ border: 2px solid #fff; }}")
            btn.clicked.connect(lambda checked, c=color: self.set_color_from_palette(c))
            btn.setToolTip(color.name())
            palette_grid.addWidget(btn, i // 4, i % 4)
            self.palette_buttons.append(btn)

        content_layout.addLayout(palette_grid)

        recent_label = QLabel("Recent Colors:")
        content_layout.addWidget(recent_label)

        self.recent_colors_layout = QHBoxLayout()
        self.recent_colors_layout.setSpacing(2)
        self.recent_color_buttons = []

        for i in range(8):
            btn = QPushButton()
            btn.setFixedSize(25, 25)
            btn.setStyleSheet("QPushButton { background-color: #333; border: 1px solid #666; }")
            btn.setEnabled(False)
            btn.hide()  # Hide initially
            self.recent_colors_layout.addWidget(btn)
            self.recent_color_buttons.append(btn)

        self.recent_colors_layout.addStretch()
        content_layout.addLayout(self.recent_colors_layout)

        color_layout.addWidget(self.color_picker_content)

        self.color_section.setLayout(color_layout)
        parent_layout.addWidget(self.color_section)

        self.color_picker_visible = True

    def toggle_color_picker_visibility(self):
        """Toggle the visibility of the color picker content"""
        self.color_picker_visible = not self.color_picker_visible
        self.color_picker_content.setVisible(self.color_picker_visible)

        if self.color_picker_visible:
            self.color_picker_toggle_btn.setText("▼ Hide")
        else:
            self.color_picker_toggle_btn.setText("▶ Show")

    def auto_show_hide_color_picker(self, tool_name):
        """Automatically show/hide color picker based on tool selection"""
        color_tools = ["paintbrush", "airbrush", "paint_bucket", "rectangle", "circle", "line", "text"]

        should_show = tool_name in color_tools

        if should_show and not self.color_picker_visible:
            self.color_picker_visible = True
            self.color_picker_content.setVisible(True)
            self.color_picker_toggle_btn.setText("▼ Hide")
        elif not should_show:
            pass

    def set_color_from_palette(self, color):
        """Set the current color from a palette button click"""
        self.current_color = color
        self.update_all_color_displays()
        self.add_to_recent_colors(color)

    def add_to_recent_colors(self, color):
        """Add a color to the recent colors list"""
        for recent_color in self.recent_colors:
            if recent_color.name() == color.name():
                return

        self.recent_colors.insert(0, color)

        if len(self.recent_colors) > 8:
            self.recent_colors = self.recent_colors[:8]

        self.update_recent_colors_display()

    def update_recent_colors_display(self):
        """Update the recent colors button display"""
        for i, btn in enumerate(self.recent_color_buttons):
            if i < len(self.recent_colors):
                color = self.recent_colors[i]
                btn.setStyleSheet(f"QPushButton {{ background-color: {color.name()}; border: 1px solid #333; }} QPushButton:hover {{ border: 2px solid #fff; }}")
                btn.setEnabled(True)
                btn.show()
                btn.setToolTip(color.name())
                try:
                    btn.clicked.disconnect()
                except:
                    pass
                btn.clicked.connect(lambda checked, c=color: self.set_color_from_palette(c))
            else:
                btn.hide()

    def update_all_color_displays(self):
        """Update all color display buttons to show the current color"""
        color_style = f"QPushButton {{ background-color: {self.current_color.name()}; border: 2px solid #666; }}"

        self.brush_color_button.setStyleSheet(color_style)
        self.shape_color_button.setStyleSheet(color_style)
        self.text_color_button.setStyleSheet(color_style)
        self.bucket_color_button.setStyleSheet(color_style)

        main_style = f"QPushButton {{ background-color: {self.current_color.name()}; border: 2px solid #666; }}"
        self.main_color_button.setStyleSheet(main_style)

        self.brush_color_button.update()
        self.shape_color_button.update()
        self.text_color_button.update()
        self.bucket_color_button.update()
        self.main_color_button.update()

    def choose_color(self):
        """Open color picker dialog"""
        color = QColorDialog.getColor(self.current_color, self, "Choose Color")
        if color.isValid():
            self.current_color = color
            self.update_all_color_displays()
            self.add_to_recent_colors(color)

    def update_right_panel_for_filter(self, filter_name):
        """Switch the right panel to show settings for the selected filter"""
        filter_to_panel = {
            "brightness_contrast": self.brightness_contrast_settings_index,
            "blur": self.blur_settings_index,
            "sharpen": self.sharpen_settings_index,
            "hue_saturation": self.hue_saturation_settings_index,
            "invert": self.invert_settings_index,
            "grayscale": self.grayscale_settings_index,
        }

        panel_index = filter_to_panel.get(filter_name, self.brightness_contrast_settings_index)
        self.options_stack.setCurrentIndex(panel_index)

        filter_titles = {
            "brightness_contrast": "Brightness/Contrast",
            "blur": "Blur Filter",
            "sharpen": "Sharpen Filter",
            "hue_saturation": "Hue/Saturation",
            "invert": "Invert Colors",
            "grayscale": "Grayscale Filter",
        }
        self.right_dock.setWindowTitle(filter_titles.get(filter_name, "Filter Options"))

    def update_right_panel_for_tool(self, tool_name):
        """Switch the right panel to show settings for the selected tool"""
        tool_to_panel = {
            "paintbrush": self.brush_settings_index,
            "airbrush": self.brush_settings_index,
            "eraser": self.eraser_settings_index,
            "paint_bucket": self.bucket_settings_index,
            "rectangle": self.shape_settings_index,
            "circle": self.shape_settings_index,
            "line": self.shape_settings_index,
            "text": self.text_settings_index,
            "selection": self.selection_settings_index,
            "color_picker": self.color_picker_settings_index,
        }

        panel_index = tool_to_panel.get(tool_name, self.brush_settings_index)
        self.options_stack.setCurrentIndex(panel_index)

        tool_titles = {
            "paintbrush": "Paintbrush Options",
            "airbrush": "Airbrush Options",
            "eraser": "Eraser Options",
            "paint_bucket": "Paint Bucket Options",
            "rectangle": "Rectangle Options",
            "circle": "Circle Options",
            "line": "Line Options",
            "text": "Text Options",
            "selection": "Selection Tool",
            "color_picker": "Eyedropper Tool",
        }
        self.right_dock.setWindowTitle(tool_titles.get(tool_name, "Tool Options"))

    def setup_toggle_buttons(self):

        self.top_toolbar = QToolBar("Toggle Panels")
        self.addToolBar(Qt.TopToolBarArea, self.top_toolbar)

        self.left_toolbar_button = QAction(QIcon(), "Drawing Tools", self)
        self.left_toolbar_button.setCheckable(True)
        self.left_toolbar_button.setChecked(True)
        self.left_toolbar_button.triggered.connect(self.toggle_left_toolbar_visibility)
        self.top_toolbar.addAction(self.left_toolbar_button)

        self.right_dock_button = QAction(QIcon(), "Options Panel", self)
        self.right_dock_button.setCheckable(True)
        self.right_dock_button.setChecked(True)
        self.right_dock_button.triggered.connect(self.toggle_right_dock_visibility)
        self.top_toolbar.addAction(self.right_dock_button)

        self.left_toolbar.visibilityChanged.connect(self.sync_left_toolbar_button)
        self.right_dock.visibilityChanged.connect(self.sync_right_dock_button)

    def sync_left_toolbar_button(self, visible):
        """Sync the left toolbar button state with actual visibility"""
        self.left_toolbar_button.setChecked(visible)
        self.left_toolbar_visible = visible

    def sync_right_dock_button(self, visible):
        """Sync the right dock button state with actual visibility"""
        self.right_dock_button.setChecked(visible)
        self.right_dock_visible = visible

    def setup_menu_bar(self):

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        view_menu = menu_bar.addMenu("&View")
        toggle_left_toolbar_action = self.left_toolbar.toggleViewAction()
        toggle_left_toolbar_action.setText("Toggle Drawing Tools")
        view_menu.addAction(toggle_left_toolbar_action)

        toggle_right_dock_action = self.right_dock.toggleViewAction()
        toggle_right_dock_action.setText("Toggle Options Panel")
        view_menu.addAction(toggle_right_dock_action)

        toggle_top_toolbar_action = self.top_toolbar.toggleViewAction()
        toggle_top_toolbar_action.setText("Toggle Panel Buttons")
        view_menu.addAction(toggle_top_toolbar_action)

