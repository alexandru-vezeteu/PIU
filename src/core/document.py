"""
Document class that wraps QGraphicsScene and manages command history.

This is the central state manager for the paint application.
"""

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QRectF
from src.core.command_history import CommandHistory
from src.core.command import ICommand


class Document:
    """
    Document manages the canvas state and command history.
    
    All operations on the canvas should go through execute_command()
    to ensure they can be undone/redone.
    """
    
    def __init__(self, width=1920, height=1080):
        """
        Initialize document with scene and command history.
        
        Args:
            width: Canvas width in pixels (default: 1920)
            height: Canvas height in pixels (default: 1080)
        """
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, width, height)
        self.history = CommandHistory(max_undo=20)
        self.width = width
        self.height = height
    
    def execute_command(self, command: ICommand):
        """
        Execute a command and add to history.
        
        Args:
            command: The command to execute
        """
        self.history.execute(command, self.scene)
    
    def undo(self) -> bool:
        """
        Undo the last command.
        
        Returns:
            bool: True if undo was performed
        """
        return self.history.undo(self.scene)
    
    def redo(self) -> bool:
        """
        Redo the last undone command.
        
        Returns:
            bool: True if redo was performed
        """
        return self.history.redo(self.scene)
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self.history.can_undo()
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self.history.can_redo()
    
    def get_undo_name(self) -> str:
        """Get name of command that would be undone."""
        return self.history.get_undo_name()
    
    def get_redo_name(self) -> str:
        """Get name of command that would be redone."""
        return self.history.get_redo_name()
    
    def clear_history(self):
        """Clear all undo/redo history."""
        self.history.clear()
