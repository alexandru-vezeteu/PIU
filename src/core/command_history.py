"""
Command history manager for undo/redo functionality.

Maintains two stacks (undo and redo) and manages command execution.
"""

from typing import List
from src.core.command import ICommand


class CommandHistory:
    """Manages undo/redo command stacks."""
    
    def __init__(self, max_undo: int = 100):
        """
        Initialize command history.
        
        Args:
            max_undo: Maximum number of commands to keep in undo stack
        """
        self.undo_stack: List[ICommand] = []
        self.redo_stack: List[ICommand] = []
        self.max_undo = max_undo
    
    def execute(self, command: ICommand, scene):
        """
        Execute a command and add to undo stack.
        
        Args:
            command: Command to execute
            scene: QGraphicsScene to operate on
        """
        command.execute(scene)
        self.undo_stack.append(command)
        self.redo_stack.clear()
        if len(self.undo_stack) > self.max_undo:
            self.undo_stack.pop(0)
    
    def undo(self, scene) -> bool:
        """
        Undo the last command.
        
        Args:
            scene: QGraphicsScene to operate on
            
        Returns:
            bool: True if undo was performed, False if nothing to undo
        """
        if not self.can_undo():
            return False
        
        command = self.undo_stack.pop()
        command.undo(scene)
        self.redo_stack.append(command)
        return True
    
    def redo(self, scene) -> bool:
        """
        Redo the last undone command.
        
        Args:
            scene: QGraphicsScene to operate on
            
        Returns:
            bool: True if redo was performed, False if nothing to redo
        """
        if not self.can_redo():
            return False
        
        command = self.redo_stack.pop()
        command.execute(scene)
        self.undo_stack.append(command)
        return True
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self.redo_stack) > 0
    
    def get_undo_name(self) -> str:
        """Get name of command that would be undone."""
        if self.can_undo():
            return self.undo_stack[-1].get_name()
        return ""
    
    def get_redo_name(self) -> str:
        """Get name of command that would be redone."""
        if self.can_redo():
            return self.redo_stack[-1].get_name()
        return ""
    
    def clear(self):
        """Clear all command history."""
        self.undo_stack.clear()
        self.redo_stack.clear()
