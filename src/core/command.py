"""
Command pattern interface for undo/redo functionality.

All operations that should be undoable must implement ICommand.
"""

from abc import ABC, abstractmethod


class ICommand(ABC):
    """Interface for undoable commands."""
    
    @abstractmethod
    def execute(self, scene):
        """
        Execute the command.
        
        Args:
            scene: QGraphicsScene to operate on
        """
        pass
    
    @abstractmethod
    def undo(self, scene):
        """
        Undo the command.
        
        Args:
            scene: QGraphicsScene to operate on
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the command name for display in history.
        
        Returns:
            str: Human-readable command name
        """
        pass
