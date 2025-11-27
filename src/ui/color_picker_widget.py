from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QGroupBox, QFrame, QColorDialog)
from PyQt5.QtGui import QColor


class ColorPickerWidget(QWidget):
    def __init__(self, current_color, parent=None):
        super().__init__(parent)
        self.current_color = current_color
        self.color_palette = [
            QColor(0, 0, 0),
            QColor(255, 255, 255),
            QColor(255, 0, 0),
            QColor(0, 255, 0),
            QColor(0, 0, 255),
            QColor(255, 255, 0),
            QColor(255, 0, 255),
            QColor(0, 255, 255),
        ]
        self.recent_colors = []
        self.visible = True
        self.color_change_callback = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)

        self.color_section = QGroupBox("Color Picker")
        color_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        self.toggle_btn = QPushButton("▼ Hide")
        self.toggle_btn.setFixedWidth(80)
        self.toggle_btn.setStyleSheet("QPushButton { background-color: transparent; border: none; text-align: left; }")
        self.toggle_btn.clicked.connect(self.toggle_visibility)

        header_layout.addWidget(QLabel("<b>Color Picker</b>"))
        header_layout.addStretch()
        header_layout.addWidget(self.toggle_btn)

        color_layout.addLayout(header_layout)

        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)

        current_color_layout = QHBoxLayout()
        current_color_layout.addWidget(QLabel("Current Color:"))

        self.main_color_button = QPushButton()
        self.main_color_button.setFixedSize(80, 40)
        self.main_color_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.current_color.name()}; border: 2px solid #666; }}"
        )
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
            btn.setStyleSheet(
                f"QPushButton {{ background-color: {color.name()}; border: 1px solid #333; }} "
                f"QPushButton:hover {{ border: 2px solid #fff; }}"
            )
            btn.clicked.connect(lambda checked, c=color: self.set_color(c))
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
            btn.hide()
            self.recent_colors_layout.addWidget(btn)
            self.recent_color_buttons.append(btn)

        self.recent_colors_layout.addStretch()
        content_layout.addLayout(self.recent_colors_layout)

        color_layout.addWidget(self.content_widget)

        self.color_section.setLayout(color_layout)
        main_layout.addWidget(self.color_section)

    def toggle_visibility(self):
        self.visible = not self.visible
        self.content_widget.setVisible(self.visible)
        self.toggle_btn.setText("Hide" if self.visible else "Show")

    def auto_show_for_tool(self, tool_name):
        color_tools = ["paintbrush", "airbrush", "paint_bucket", "rectangle", "circle", "line", "text"]
        should_show = tool_name in color_tools

        if should_show and not self.visible:
            self.visible = True
            self.content_widget.setVisible(True)
            self.toggle_btn.setText("▼ Hide")

    def set_color(self, color):
        self.current_color = color
        self.main_color_button.setStyleSheet(
            f"QPushButton {{ background-color: {color.name()}; border: 2px solid #666; }}"
        )
        self.main_color_button.update()
        self.add_to_recent_colors(color)
        if self.color_change_callback:
            self.color_change_callback(color)

    def choose_color(self):
        color = QColorDialog.getColor(self.current_color)
        if color.isValid():
            self.set_color(color)

    def add_to_recent_colors(self, color):
        for recent_color in self.recent_colors:
            if recent_color.name() == color.name():
                return

        self.recent_colors.insert(0, color)
        if len(self.recent_colors) > 8:
            self.recent_colors = self.recent_colors[:8]

        self.update_recent_colors_display()

    def update_recent_colors_display(self):
        for i, btn in enumerate(self.recent_color_buttons):
            if i < len(self.recent_colors):
                color = self.recent_colors[i]
                btn.setStyleSheet(
                    f"QPushButton {{ background-color: {color.name()}; border: 1px solid #333; }} "
                    f"QPushButton:hover {{ border: 2px solid #fff; }}"
                )
                btn.setEnabled(True)
                btn.show()
                btn.setToolTip(color.name())
                try:
                    btn.clicked.disconnect()
                except:
                    pass
                btn.clicked.connect(lambda checked, c=color: self.set_color(c))
            else:
                btn.hide()

    def get_current_color(self):
        return self.current_color

    def set_color_change_callback(self, callback):
        self.color_change_callback = callback
