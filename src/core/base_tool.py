from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.QtGui import QIcon
from src.core.base_action import BaseAction


class BaseTool(BaseAction):
    def __init__(self, name, icon_path=None):
        super().__init__(name, icon_path)

    @abstractmethod
    def create_action(self) -> QAction:
        pass

    @abstractmethod
    def create_settings_panel(self) -> QWidget:
        pass

    @abstractmethod
    def get_tool_name(self) -> str:
        """Return unique identifier for this tool."""
        pass

    def get_action_name(self) -> str:
        """Alias for get_tool_name to match BaseAction interface."""
        return self.get_tool_name()

    def needs_color(self) -> bool:
        return False
    
    def register_bindings(self, bind_func):
        """
        Override this to register key+mouse combinations for this tool.
        Default implementation does nothing.
        """
        pass

    def on_tool_selected(self):
        """Called when this tool becomes active."""
        self.on_action_selected()

    def on_tool_deselected(self):
        """Called when this tool is no longer active."""
        self.on_action_deselected()

    def mouse_press_event(self, event, scene, view=None):
        """Called when mouse is pressed on canvas"""
        pass

    def mouse_move_event(self, event, scene, view=None):
        """Called when mouse is moved on canvas"""
        pass

    def mouse_release_event(self, event, scene, view=None):
        """Called when mouse is released on canvas"""
        pass
