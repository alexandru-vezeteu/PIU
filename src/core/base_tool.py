from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.QtGui import QIcon


class BaseTool(ABC):
    def __init__(self, name, icon_path=None):
        self.name = name
        self.icon_path = icon_path
        self._action = None
        self._settings_widget = None

    @abstractmethod
    def create_action(self) -> QAction:
        pass

    @abstractmethod
    def create_settings_panel(self) -> QWidget:
        pass

    @abstractmethod
    def get_tool_name(self) -> str:
        pass

    def get_action(self) -> QAction:
        return self._action

    def get_settings_widget(self) -> QWidget:
        return self._settings_widget

    def needs_color(self) -> bool:
        return False

    def on_tool_selected(self):
        pass

    def on_tool_deselected(self):
        pass

    def mouse_press_event(self, event, scene, view=None):
        """Called when mouse is pressed on canvas"""
        pass

    def mouse_move_event(self, event, scene, view=None):
        """Called when mouse is moved on canvas"""
        pass

    def mouse_release_event(self, event, scene, view=None):
        """Called when mouse is released on canvas"""
        pass
