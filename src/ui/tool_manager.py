from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtCore import Qt


class ToolManager:
    def __init__(self):
        self.tools = []
        self.current_tool = None
        self.tool_selection_callback = None

    def register_tool(self, tool):
        self.tools.append(tool)

    def get_tools(self):
        return self.tools

    def select_tool(self, tool_name):
        for tool in self.tools:
            if tool.get_tool_name() == tool_name:
                if self.current_tool:
                    self.current_tool.on_tool_deselected()
                self.current_tool = tool
                tool.on_tool_selected()
                self.update_tool_actions(tool_name)
                if self.tool_selection_callback:
                    self.tool_selection_callback(tool)
                break

    def update_tool_actions(self, selected_tool_name):
        for tool in self.tools:
            action = tool.get_action()
            if action:
                action.setChecked(tool.get_tool_name() == selected_tool_name)

    def get_current_tool(self):
        return self.current_tool

    def set_tool_selection_callback(self, callback):
        self.tool_selection_callback = callback

    def get_tool_by_name(self, tool_name):
        for tool in self.tools:
            if tool.get_tool_name() == tool_name:
                return tool
        return None
