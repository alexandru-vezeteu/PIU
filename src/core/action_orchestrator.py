"""
Action Orchestrator - Central hub for managing input bindings.

This orchestrator knows which action (tool/filter) to call based on
keyboard+mouse events and their registered bindings.
"""

from PyQt5.QtCore import Qt


class ActionOrchestrator:
    """Manages all action bindings and routes input events to the correct action."""
    
    def __init__(self):
        self.actions = []  # All registered actions (tools, filters, etc)
        self.bindings = []  # List of binding dictionaries
        self.current_action = None  # Currently active action
        self.action_selection_callback = None
    
    def register_action(self, action):
        """Register an action (tool or filter) and its bindings."""
        self.actions.append(action)
        action.register_bindings(self.bind)
    
    def bind(self, modifiers, mouse_button, callback, key=None):
        """
        Register an input combination to a callback.
        
        Args:
            modifiers: frozenset of modifier keys (Qt.Key_Control, etc) or None
            mouse_button: Qt.LeftButton, Qt.RightButton, etc or None  
            callback: function to call when this combo is triggered
            key: optional keyboard key (e.g. 'B', 'E') for keyboard-only shortcuts
        """
        self.bindings.append({
            'modifiers': modifiers,
            'mouse_button': mouse_button,
            'key': key,
            'callback': callback
        })
        print(f"[Orchestrator] Registered binding: mods={modifiers}, mouse={mouse_button}, key={key}")
    
    def find_binding(self, modifiers, mouse_button=None, key=None):
        """
        Find a binding that matches the given input combo.
        
        Args:
            modifiers: frozenset of currently pressed modifier keys or None
            mouse_button: which mouse button was pressed or None
            key: which key was pressed or None
            
        Returns:
            callback function or None
        """
        for binding in self.bindings:
            if binding['modifiers'] != modifiers:
                continue
            
            if binding['mouse_button'] is not None:
                if binding['mouse_button'] != mouse_button:
                    continue
            
            if binding['key'] is not None:
                if binding['key'] != key:
                    continue
            
            return binding['callback']
        
        return None
    
    def get_current_modifiers(self, event):
        """Extract modifier keys from an event into a frozenset."""
        mods = set()
        if event.modifiers() & Qt.ControlModifier:
            mods.add(Qt.Key_Control)
        if event.modifiers() & Qt.ShiftModifier:
            mods.add(Qt.Key_Shift)
        if event.modifiers() & Qt.AltModifier:
            mods.add(Qt.Key_Alt)
        return frozenset(mods) if mods else None
    
    def handle_mouse_press(self, event, scene, view):
        """Handle mouse press - check for bindings first, then default to current action."""
        modifiers = self.get_current_modifiers(event)
        mouse_button = event.button()
        
        binding_callback = self.find_binding(modifiers, mouse_button)
        if binding_callback:
            print(f"[Orchestrator] Matched binding for {modifiers} + {mouse_button}")
            return binding_callback(event, scene, view)
        
        if self.current_action and hasattr(self.current_action, 'mouse_press_event'):
            return self.current_action.mouse_press_event(event, scene, view)
        
        return None
    
    def handle_mouse_move(self, event, scene, view):
        """Handle mouse move - delegate to current action."""
        if self.current_action and hasattr(self.current_action, 'mouse_move_event'):
            return self.current_action.mouse_move_event(event, scene, view)
        return None
    
    def handle_mouse_release(self, event, scene, view):
        """Handle mouse release - delegate to current action."""
        if self.current_action and hasattr(self.current_action, 'mouse_release_event'):
            return self.current_action.mouse_release_event(event, scene, view)
        return None
    
    def handle_wheel_event(self, event, scene, view):
        """Handle mouse wheel events - check for Ctrl modifier for zoom."""
        modifiers = self.get_current_modifiers(event)
        
        if modifiers and Qt.Key_Control in modifiers:
            zoom_tool = None
            for action in self.actions:
                if hasattr(action, 'get_tool_name') and action.get_tool_name() == 'zoom':
                    zoom_tool = action
                    break
            
            if zoom_tool and hasattr(zoom_tool, 'editor'):
                if event.angleDelta().y() > 0:
                    zoom_tool.editor.zoom_in()
                else:
                    zoom_tool.editor.zoom_out()
                event.accept()
                return True
        
        return False
    
    def handle_key_press(self, event):
        """Handle keyboard press - check for key bindings."""
        modifiers = self.get_current_modifiers(event)
        key = event.text().upper() if event.text() else None
        
        if key:
            binding_callback = self.find_binding(modifiers, key=key)
            if binding_callback:
                print(f"[Orchestrator] Matched key binding for {modifiers} + '{key}'")
                binding_callback()
                return True
        
        return False
    
    def select_action(self, action_name):
        """Select an action by name."""
        for action in self.actions:
            if action.get_tool_name() == action_name:
                if self.current_action:
                    self.current_action.on_tool_deselected()
                self.current_action = action
                action.on_tool_selected()
                self.update_action_states(action_name)
                if self.action_selection_callback:
                    self.action_selection_callback(action)
                break
    
    def update_action_states(self, selected_action_name):
        """Update UI state of all actions."""
        for action in self.actions:
            ui_action = action.get_action()
            if ui_action:
                ui_action.setChecked(action.get_tool_name() == selected_action_name)
    
    def get_current_action(self):
        return self.current_action
    
    def get_actions(self):
        return self.actions
    
    def set_action_selection_callback(self, callback):
        self.action_selection_callback = callback
