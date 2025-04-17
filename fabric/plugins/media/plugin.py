from utils.plugins import ToolbarPlugin
from widgets.common_button import CommonButton


class InternetStatus(ToolbarPlugin):
    def __init__(self):
        self._name = "media"
        self._description = "Show media button."

        self.shell_context = None

    def initialize(self, shell_context):
        self.shell_context = shell_context

    def register_toolbar_widget(self):
        return CommonButton(name="media-button", icon="vinyl", title="Nothing playing")
