from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.QtGui import QIcon


class BaseFilter(ABC):
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
    def get_filter_name(self) -> str:
        pass

    @abstractmethod
    def apply_filter(self, image):
        pass

    def get_action(self) -> QAction:
        return self._action

    def get_settings_widget(self) -> QWidget:
        return self._settings_widget
