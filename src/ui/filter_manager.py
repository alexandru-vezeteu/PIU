class FilterManager:
    def __init__(self):
        self.filters = []
        self.current_filter = None
        self.filter_selection_callback = None
        self.filters_expanded = False

    def register_filter(self, filter_obj):
        self.filters.append(filter_obj)

    def get_filters(self):
        return self.filters

    def select_filter(self, filter_name):
        for filter_obj in self.filters:
            if filter_obj.get_filter_name() == filter_name:
                self.current_filter = filter_obj
                self.update_filter_actions(filter_name)
                if self.filter_selection_callback:
                    self.filter_selection_callback(filter_obj)
                break

    def update_filter_actions(self, selected_filter_name):
        for filter_obj in self.filters:
            action = filter_obj.get_action()
            if action:
                action.setChecked(filter_obj.get_filter_name() == selected_filter_name)

    def get_current_filter(self):
        return self.current_filter

    def set_filter_selection_callback(self, callback):
        self.filter_selection_callback = callback

    def toggle_expanded(self):
        self.filters_expanded = not self.filters_expanded
        return self.filters_expanded
    
    def get_filter_by_name(self, filter_name):
        """Get a filter by its name."""
        for filter_obj in self.filters:
            if filter_obj.get_filter_name() == filter_name:
                return filter_obj
        return None

    def is_expanded(self):
        return self.filters_expanded
