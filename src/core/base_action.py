"""
Base action class that both Tools and Filters inherit from.

This provides a common interface for anything that can be triggered
by user input (keyboard, mouse, or both).
"""

from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QWidget, QAction


class BaseAction(ABC):
    """Base class for all user-triggerable actions (tools, filters, etc)."""
    
    def __init__(self, name, icon_path=None):
        self.name = name
        self.icon_path = icon_path
        self._action = None
        self._settings_widget = None
    
    @abstractmethod
    def create_action(self) -> QAction:
        """Create toolbar/menu action for this."""
        pass
    
    @abstractmethod
    def create_settings_panel(self) -> QWidget:
        """Create settings panel widget."""
        pass
    
    @abstractmethod
    def get_action_name(self) -> str:
        """Return unique identifier for this action."""
        pass
    
    def get_action(self) -> QAction:
        return self._action
    
    def get_settings_widget(self) -> QWidget:
        return self._settings_widget
    
    def register_bindings(self, bind_func):
        """
        Register input combinations that trigger this action.
        
        Args:
            bind_func: Function to call: bind_func(modifiers, mouse_button, callback)
                      modifiers: frozenset of Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt or None
                      mouse_button: Qt.LeftButton, Qt.RightButton, Qt.MiddleButton, or None
                      callback: method to call when combo is triggered (event, scene, view)
        
        Example:
            bind_func(frozenset([Qt.Key_Control]), Qt.LeftButton, self.on_ctrl_click)
            
            bind_func(frozenset([Qt.Key_Alt]), Qt.LeftButton, self.on_alt_drag)
            
            bind_func(None, None, self.activate, key='B')
        """
        pass
    
    def on_action_selected(self):
        """Called when this action becomes active."""
        pass
    
    def on_action_deselected(self):
        """Called when this action is no longer active."""
        pass
