import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QToolBar,
    QAction, QDockWidget, QWidget, QVBoxLayout, QLabel, QSlider, QMenuBar, QMenu
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QIcon
class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 1200, 800)

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

    def toggle_left_toolbar_visibility(self):
        self.left_toolbar_visible = not self.left_toolbar_visible
        self.left_toolbar.setVisible(self.left_toolbar_visible)
        
    def setup_left_toolbar(self):

        self.left_toolbar = QToolBar("Drawing Tools")
        self.left_toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, self.left_toolbar)

   
        # path/to/icon.png
        action_paintbrush = QAction(QIcon(), "Paintbrush", self)
        action_airbrush = QAction(QIcon(), "Airbrush", self)
        action_paint_bucket = QAction(QIcon(), "Paint Bucket", self)
        action_color_picker = QAction(QIcon(), "Color Picker", self)

        self.left_toolbar.addAction(action_paintbrush)
        self.left_toolbar.addAction(action_airbrush)
        self.left_toolbar.addAction(action_paint_bucket)
        self.left_toolbar.addSeparator()
        self.left_toolbar.addAction(action_color_picker)
    def toggle_right_dock_visibility(self):
        self.right_dock_visible = not self.right_dock_visible
        self.right_dock.setVisible(self.right_dock_visible)
        
    def setup_right_dock(self):
        self.right_dock = QDockWidget("Tool/Filter Options", self)
        self.right_dock.setAllowedAreas(Qt.RightDockWidgetArea)

        options_widget = QWidget()
        layout = QVBoxLayout(options_widget)

        self.brightness_label = QLabel("Brightness: 50")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(50)
        self.brightness_slider.valueChanged.connect(lambda val: self.brightness_label.setText(f"Brightness: {val}"))

        self.contrast_label = QLabel("Contrast: 50")
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 100)
        self.contrast_slider.setValue(50)
        self.contrast_slider.valueChanged.connect(lambda val: self.contrast_label.setText(f"Contrast: {val}"))

        layout.addWidget(self.brightness_label)
        layout.addWidget(self.brightness_slider)
        layout.addWidget(self.contrast_label)
        layout.addWidget(self.contrast_slider)
        layout.addStretch()

        self.right_dock.setWidget(options_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)

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

        filters_menu = menu_bar.addMenu("&Filters")
        filters_menu.addAction("Brightness/Contrast")
        filters_menu.addAction("Blur")
        filters_menu.addAction("Sharpen")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec_())